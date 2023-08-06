# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "04/03/2019"


from silx.utils.enum import Enum as _Enum
from ...utils import _assert_param_instance
from .anglemode import CorAngleMode
from tomwer.core.utils import getParametersFromParOrInfo
from .projectiontype import ProjectionType
from .mode import AxisMode
from collections import namedtuple
from silx.io.url import DataUrl
import silx.io.utils
import logging
import numpy
import os
import h5py
from typing import Union
from tomwer.core.process.baseprocess import BaseProcess

try:
    from nabu.preproc.phase import PaganinPhaseRetrieval, PaddingMode
except ImportError:
    from tomwer.third_party.nabu.preproc.phase import PaganinPhaseRetrieval, PaddingMode

_logger = logging.getLogger(__name__)


_calculation_conf = namedtuple(
    "_calculation_conf", ["projection_type", "paganin"]
)  # noqa

_WITH_PAG = "withpag"
_NO_PAG = "nopag"


class AxisCalculationInput(_Enum):
    """Define the different mode of input the user can have for axis calculation"""

    emission = _calculation_conf(ProjectionType.absorption, False)
    transmission = _calculation_conf(ProjectionType.transmission, False)
    transmission_pag = _calculation_conf(ProjectionType.transmission, True)

    def name(self):
        if self.value.paganin is True:
            return " ".join((self.value.projection_type.value, "paganin"))
        else:
            return self.value.projection_type.value

    def to_dict(self):
        pag_text = _WITH_PAG if self.value.paganin is True else _NO_PAG
        return "_".join((self.value.projection_type.value, pag_text))

    @classmethod
    def from_value(cls, value):
        if type(value) is str and len(value.split("_")) == 2:
            proj_type, pag = value.split("_")
            value_pag = True if pag == _WITH_PAG else False
            value_proj = ProjectionType.from_value(proj_type)
            return cls.from_value(_calculation_conf(value_proj, value_pag))
        elif isinstance(value, cls):
            return value
        else:
            for member in cls:
                if value in (member.value, member.name()):
                    return member
            raise ValueError("Cannot convert: %s" % value)


class AxisResource(object):
    """Helper for axis file relative stuff"""

    _PAGANIN_CONFIG = {"distance": 100e-3, "energy": 35, "delta_beta": 1e3}
    """Paganin configuration for axis calculation. To simplify we have only one
    static configuration for now. Otherwise complicate stuff"""

    def __init__(self, url):
        assert url is None or isinstance(url, DataUrl)
        assert url is None or url.is_valid()
        self.__url = url
        self.__raw_data = None
        self.__norme_data = None
        self.__norm_paganin = None

    @property
    def url(self):
        return self.__url

    @property
    def data(self):
        """

        :return: 2D numpy.array
        """
        if self.__url is None:
            return None
        if self.__raw_data is None:
            self.__raw_data = silx.io.utils.get_data(self.url)
        return self.__raw_data

    @data.setter
    def data(self, data):
        self.__raw_data = data

    @property
    def normalized_data(self):
        return self.__norme_data

    @normalized_data.setter
    def normalized_data(self, data):
        self.__norme_data = data

    def normalize_data(self, scan, log_):
        """Normalize data for axis calculation"""
        if self.__url is None:
            return None
        else:
            self.__norme_data = scan.flat_field_correction(data=self.data)
            if log_ is True:
                self.__norme_data[
                    numpy.isnan(self.__norme_data)
                ] = self.__norme_data.max()
                if self.__norme_data.max() < 0:
                    _logger.error("max data value < 0 unable to compute log")
                else:
                    try:
                        data = self.__norme_data
                        data[data <= 1] = 1
                        self.__norme_data = -numpy.log(data)
                    except Exception as e:
                        _logger.error("Fail to apply log on radio" + e)
            else:
                self.__norme_data[
                    numpy.isnan(self.__norme_data)
                ] = self.__norme_data.min()

        return self.__norme_data

    @property
    def normalized_data_paganin(self):
        """

        :return: data processed by the pagagnin phase retrieval
        :rtype: 2D numpy.array
        """
        if self.__url is None:
            return None
        if self.__norm_paganin is None:
            if self.normalized_data is None:
                raise ValueError("data should be normalized before applying " "paganin")
            else:
                data = self.normalized_data
                phase_retrieval = PaganinPhaseRetrieval(
                    data.shape, **AxisResource._PAGANIN_CONFIG
                )
                self.__norm_paganin = phase_retrieval.apply_filter(data)
        return self.__norm_paganin

    @normalized_data_paganin.setter
    def normalized_data_paganin(self, data):
        self.__norm_paganin = data

    def __eq__(self, other):
        if not isinstance(other, AxisResource):
            return False
        if self.url is None and other.url is None:
            return True
        elif self.url is None or other.url is None:
            return False
        else:
            return self.url == other.url


class AxisRP:
    """
    Configuration class for a tomwer :class:`AxisProcess`

    note: every modification on the parameters will process a call fo changed
    except `axis_url_1` and `axis_url_2` which will produce a call to the
    dedicated axis_url_changed
    """

    AXIS_POSITION_PAR_KEY = "ROTATION_AXIS_POSITION"
    """Key used for the axis position in par files"""

    def __init__(self):
        self.__mode = AxisMode.centered
        """Mode used for defining the COR (center of rotation)"""
        self.__value_ref_tomwer = None
        """Value of the center of rotation in [0; image_width].
        None is not processing"""
        self.__value_ref_nabu = None
        """Value of the center of rotation in [-image_width/2; image_width/2].
        None is not processing"""
        self.__angle_mode = CorAngleMode.use_0_180
        """Angle to use for radios"""
        self.__estimated_cor = 0.0
        """Position to use for near calculation"""
        self.__axis_url_1 = AxisResource(url=None)
        """first data url to use for axis cor calculation"""
        self.__axis_url_2 = AxisResource(url=None)
        """second data url to use for axis cor calculation"""
        self.__calculation_input_type = AxisCalculationInput.transmission
        """Type of input (emission, absorption, with or without paganin)"""
        self.__use_sinogram = False
        """Do we want to use the sinogram of the radios for computing center
        of rotation"""
        self.__sinogram_line = None
        """Line of the radios to use for getting the sinogram"""
        self.__sinogram_subsampling = 1
        """if use sinogram activate, we can use a subsampling to reduce
        computation time"""
        self.__look_at_stdmax = False
        """do the near search at X position which as the max Y column standard
        deviation"""
        self.__near_wx = 5
        """do the near search in an X window of size +-near_wx"""
        self.__fine_stepx = 0.1
        """shift step x for fine shifting image"""
        self.__scale_img2_to_img1 = False
        """do image scaling"""
        self.__padding_mode = None
        self.__frame_width = None
        self.__side = "all"
        """side of the cor. Requested by nabu cor algorithms growing-window
        and sliding-window"""

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, mode):
        if isinstance(mode, str):
            try:
                name = mode
                if name in ("global_", "global"):
                    name = AxisMode.global_.name
                elif name == "accurate":
                    _logger.info(
                        "convert axis mode {} to {} (renamed)"
                        "".format(name, AxisMode.centered.name)
                    )
                    name = AxisMode.centered.name
                _mode = getattr(AxisMode, name)
            except:
                raise ValueError("Fail to create axis mode from %s" % mode)
        else:
            _assert_param_instance(mode, AxisMode)
            _mode = mode
        self.__mode = _mode
        self.changed()

    @property
    def frame_width(self):
        return self.__frame_width

    @frame_width.setter
    def frame_width(self, value):
        self.__frame_width = value

    @property
    def angle_mode(self):
        return self.__angle_mode

    @angle_mode.setter
    def angle_mode(self, mode):
        if type(mode) is str:
            mode = CorAngleMode.from_value(mode)

        if self.__angle_mode != mode:
            self.__angle_mode = mode
            self.changed()

    @property
    def value_ref_tomwer(self):
        return self.__value_ref_tomwer

    def set_value_ref_tomwer(self, value):
        _assert_param_instance(value, (int, float, str, type(None)))
        if value is None:
            changed = self.__value_ref_tomwer != None
        elif isinstance(value, str) and value == "...":
            changed = self.__value_ref_tomwer != "..."
        else:
            changed = self.__value_ref_tomwer != float(value)
        if changed:
            if value is None or (isinstance(value, str) and value == "..."):
                self.__value_ref_tomwer = value
                self.__value_ref_nabu = value
            else:
                self.__value_ref_tomwer = float(value)
                if self.frame_width is not None:
                    self.__value_ref_nabu = (
                        self.__value_ref_tomwer + self.frame_width / 2.0
                    )
            self.changed()

    @property
    def value_ref_nabu(self):
        return self.__value_ref_tomwer

    @property
    def estimated_cor(self):
        return self.__estimated_cor

    @estimated_cor.setter
    def estimated_cor(self, value):
        if self.__estimated_cor != value:
            self.__estimated_cor = value
            self.changed()

    @property
    def side(self):
        return self.__side

    @side.setter
    def side(self, side):
        if side not in ("all", "left", "right", "center"):
            raise ValueError("side '{}' is not managed".format(side))
        if self.__side != side:
            self.__side = side
            self.changed()

    @property
    def axis_url_1(self):
        """the first file to be used for the axis calculation"""
        return self.__axis_url_1

    def _get_rsrc_frm_url(self, old_resource, new_url_):
        """
        Util function to compare new resource / url with an existing one.
        """
        new_resource = None
        changed = False
        if isinstance(new_url_, AxisResource):
            if old_resource != new_url_:
                changed = True
                new_resource = new_url_
        elif isinstance(new_url_, str):
            if new_url_ == "":
                new_resource = AxisResource(None)
            else:
                new_resource = AxisResource(DataUrl(path=new_url_))
            if old_resource != new_resource:
                changed = True
        else:
            assert isinstance(new_url_, DataUrl) or new_url_ is None
            new_resource = AxisResource(new_url_)
            if old_resource != new_resource:
                changed = True
        return new_resource, changed

    @axis_url_1.setter
    def axis_url_1(self, url_):
        new_resource, changed = self._get_rsrc_frm_url(
            old_resource=self.__axis_url_1, new_url_=url_
        )
        if changed is True:
            self.__axis_url_1 = new_resource
            self.axis_urls_changed()

    @property
    def axis_url_2(self):
        """the second file to be used for the axis calculation"""
        return self.__axis_url_2

    @axis_url_2.setter
    def axis_url_2(self, url_):
        new_resource, changed = self._get_rsrc_frm_url(
            old_resource=self.__axis_url_2, new_url_=url_
        )
        if changed is True:
            self.__axis_url_2 = new_resource
            self.axis_urls_changed()

    @property
    def projection_type(self):
        return self.__calculation_input_type.value.projection_type

    @property
    def paganin_preproc(self):
        return self.__calculation_input_type.value.paganin

    @property
    def calculation_input_type(self):
        return self.__calculation_input_type

    @calculation_input_type.setter
    def calculation_input_type(self, type_):
        assert isinstance(type_, AxisCalculationInput)
        value = AxisCalculationInput.from_value(type_)
        if value != self.__calculation_input_type:
            self.__calculation_input_type = type_
            self.changed()

    @property
    def use_sinogram(self):
        return self.__use_sinogram

    @use_sinogram.setter
    def use_sinogram(self, sinogram):
        if self.__use_sinogram != sinogram:
            self.__use_sinogram = sinogram
            self.changed()

    @property
    def sinogram_line(self):
        return self.__sinogram_line

    @sinogram_line.setter
    def sinogram_line(self, line):
        if line == "":
            if self.__sinogram_line != None:
                self.__sinogram_line = None
                self.changed()
        else:
            if line is not None:
                line = int(line)
            if self.__sinogram_line != line:
                self.__sinogram_line = line
                self.changed()

    @property
    def sinogram_subsampling(self) -> int:
        """Subsample radio to speed up processing of the sinogram generation"""
        return self.__sinogram_subsampling

    @sinogram_subsampling.setter
    def sinogram_subsampling(self, subsampling: int) -> None:
        subsampling = int(subsampling)
        if subsampling != self.__sinogram_subsampling:
            self.__sinogram_subsampling = subsampling
            self.changed()

    @property
    def look_at_stdmax(self):
        return self.__look_at_stdmax

    @look_at_stdmax.setter
    def look_at_stdmax(self, stdmax):
        self.__look_at_stdmax = stdmax

    @property
    def near_wx(self):
        return self.__near_wx

    @near_wx.setter
    def near_wx(self, width):
        if self.__near_wx != width:
            self.__near_wx = width
            self.changed()

    @property
    def fine_step_x(self):
        return self.__fine_stepx

    @fine_step_x.setter
    def fine_step_x(self, step_size):
        if self.__fine_stepx != step_size:
            self.__fine_stepx = step_size
            self.changed()

    @property
    def scale_img2_to_img1(self):
        return self.__scale_img2_to_img1

    @scale_img2_to_img1.setter
    def scale_img2_to_img1(self, scale):
        if self.__scale_img2_to_img1 != scale:
            self.__scale_img2_to_img1 = scale
            self.changed()

    @property
    def padding_mode(self):
        return self.__padding_mode

    @padding_mode.setter
    def padding_mode(self, mode):
        if self.__padding_mode != mode:
            self.__padding_mode = mode
            self.changed()

    def changed(self):
        """callback to overwrite when the paramter value changed"""
        pass

    def set_position_frm_par_file(self, file_path, entry=None, force=False):
        """Set position value from a file

        :param str file_path: path to the par file
        :param bool force: if True, force the mode to read and set
                           `position_value` to None if failed to read the file.
                           Otherwise only `mode` and `position_value` when the
                           file read succeed.
        """

        def get_position_in_file():
            if not os.path.isfile(file_path):
                raise ValueError(file_path, "is not a valid file path")

            if h5py.is_hdf5(file_path):
                return self.get_cor_position_frm_tomwer_file(
                    file_path=file_path, entry=entry
                )
            elif file_path.lower().endswith(".par") or file_path.lower().endswith(
                ".info"
            ):
                _dict = getParametersFromParOrInfo(file_path)
                if self.AXIS_POSITION_PAR_KEY.lower() not in _dict:
                    err = "fail to find `%s` in %s" % (
                        self.AXIS_POSITION_PAR_KEY,
                        file_path,
                    )
                    _logger.info(err)
                    raise KeyError(err)
                else:
                    return _dict[self.AXIS_POSITION_PAR_KEY.lower()]
            else:
                with open(file_path, mode="r") as fd:
                    l1 = fd.readline()
                    values = l1.split(" ")
                    if len(values) > 0:
                        try:
                            res = float(values[0])
                        except:
                            _logger.info(
                                "fail to load center of rotation " "from ", file_path
                            )
                            return None
                        else:
                            return res

        if force:
            try:
                position = get_position_in_file()
            except (KeyError, ValueError) as e:
                _logger.warning(e)
                position = None
        else:
            position = get_position_in_file()

        changed = self.mode != AxisMode.read or position != self.value_ref_tomwer
        self.mode = AxisMode.read
        if position is None:
            self.set_value_ref_tomwer(None)
        else:
            self.set_value_ref_tomwer(float(position))

        if changed:
            self.changed()

    @staticmethod
    def get_cor_position_frm_tomwer_file(
        file_path: str, entry=None
    ) -> Union[None, float]:
        """
        Parse the given .h5 file, looking for axis processes. If found some
        then return the first value discover

        :param str file_path: tomwer processes file (.h5)
        :return: center of rotation or none
        :rtype: Union[None, float]
        """
        from .axis import AxisProcess  # avoid cyclic import

        processes = BaseProcess.get_processes_frm_type(
            process_file=file_path, process_type=AxisProcess, entry=entry
        )
        if len(processes) == 0:
            _logger.warning("failed to find any information on center " "of rotation")
            return None
        elif len(processes) > 1:
            _logger.info("found more than one value computed for " "center of rotation")
        _logger.info(
            "load center of rotation from %s: %s"
            % (file_path, processes[0].results["center_of_rotation"])
        )
        cor = processes[0].results["center_of_rotation"]
        if cor in [None, ""]:
            return None
        else:
            return float(cor)

    def n_url(self):
        """

        :return: number of available url from url_1, url_2
        """
        n_url = 0
        if self.axis_url_1 and self.axis_url_1.url:
            n_url += 1
        if self.axis_url_2 and self.axis_url_2.url:
            n_url += 1
        return n_url

    def to_dict(self):
        # keep octave compatibility
        axis_urls_1 = self.axis_url_1.url
        if axis_urls_1 is None:
            axis_urls_1 = ""
        else:
            axis_urls_1 = axis_urls_1.path()
        axis_urls_2 = self.axis_url_2.url
        if axis_urls_2 is None:
            axis_urls_2 = ""
        else:
            axis_urls_2 = axis_urls_2.path()

        _dict = {
            "MODE": self.mode.value,
            "POSITION_VALUE": self.value_ref_tomwer,
            "CALC_INPUT_TYPE": self.calculation_input_type.to_dict(),
            "ANGLE_MODE": self.angle_mode.value,
            "USE_SINOGRAM": self.use_sinogram,
            "SINOGRAM_LINE": self.sinogram_line if self.use_sinogram else "",
            "SINOGRAM_SUBSAMPLING": self.sinogram_subsampling,
            "AXIS_URL_1": axis_urls_1,
            "AXIS_URL_2": axis_urls_2,
            "LOOK_AT_STDMAX": self.look_at_stdmax,
            "NEAR_WX": self.near_wx,
            "FINE_STEP_X": self.fine_step_x,
            "SCALE_IMG2_TO_IMG1": self.scale_img2_to_img1,
            "NEAR_POSITION": self.estimated_cor,
            "PADDING_MODE": self.padding_mode,
        }
        return _dict

    @staticmethod
    def from_dict(_dict):
        axis = AxisRP()
        axis.load_from_dict(_dict=_dict)
        return axis

    def load_from_dict(self, _dict):
        self.mode = _dict["MODE"]
        self.set_value_ref_tomwer(_dict["POSITION_VALUE"])
        self.calculation_input_type = AxisCalculationInput.from_value(
            _dict["CALC_INPUT_TYPE"]
        )
        self.use_sinogram = _dict["USE_SINOGRAM"]
        self.angle_mode = CorAngleMode.from_value(_dict["ANGLE_MODE"])
        self.sinogram_line = _dict["SINOGRAM_LINE"]
        self.axis_url_1 = _dict["AXIS_URL_1"]
        self.axis_url_2 = _dict["AXIS_URL_2"]
        self.look_at_stdmax = _dict["LOOK_AT_STDMAX"]
        self.near_wx = _dict["NEAR_WX"]
        self.fine_step_x = _dict["FINE_STEP_X"]
        self.scale_img2_to_img1 = _dict["SCALE_IMG2_TO_IMG1"]
        self.estimated_cor = float(_dict["NEAR_POSITION"])
        self.sinogram_subsampling = _dict["SINOGRAM_SUBSAMPLING"]
        if "PADDING_MODE" in _dict:
            self.padding_mode = _dict["PADDING_MODE"]

    def copy(self, axis_params, copy_axis_url=True):
        assert isinstance(axis_params, AxisRP)
        self.mode = axis_params.mode
        self.frame_width = axis_params.frame_width
        self.set_value_ref_tomwer(axis_params.value_ref_tomwer)
        self.calculation_input_type = axis_params.calculation_input_type
        self.use_sinogram = axis_params.use_sinogram
        self.angle_mode = axis_params.angle_mode
        self.sinogram_line = axis_params.sinogram_line
        self.sinogram_subsampling = axis_params.sinogram_subsampling
        self.look_at_stdmax = axis_params.look_at_stdmax
        self.near_wx = axis_params.near_wx
        self.fine_step_x = axis_params.fine_step_x
        self.scale_img2_to_img1 = axis_params.scale_img2_to_img1
        self.estimated_cor = axis_params.estimated_cor
        self.padding_mode = axis_params.padding_mode
        self.side = axis_params.side
        if copy_axis_url:
            self.axis_url_1 = axis_params.axis_url_1
            self.axis_url_2 = axis_params.axis_url_2

    def __str__(self):
        return str(self.to_dict())

    def axis_urls_changed(self):
        """Callback when the axis url change"""
        pass
