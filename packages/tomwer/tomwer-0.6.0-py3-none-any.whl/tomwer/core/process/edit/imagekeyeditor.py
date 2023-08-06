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
__date__ = "26/10/2020"


from tomoscan.esrf.hdf5scan import ImageKey as _ImageKey
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from nxtomomill.utils import change_image_key_control as _change_image_key_control
from tomwer.core.process.baseprocess import SingleProcess, _input_desc, _output_desc
from tomoscan.esrf.hdf5scan import ImageKey
from tomwer.utils import docstring
import nxtomomill.version
import logging

_logger = logging.getLogger(__name__)


IMAGE_KEYS = {
    "projection": _ImageKey.PROJECTION,
    "invalid": _ImageKey.INVALID,
    "dark": _ImageKey.DARK_FIELD,
    "flat": _ImageKey.FLAT_FIELD,
}


def change_image_key_control(scan: HDF5TomoScan, config: dict) -> TomwerScanBase:
    """

    :param scan:
    :param config:
    :raises KeyError: if 'frames_indexes' or 'image_key_control_value' are
                      not in config
    :return:
    """
    if scan is None:
        return
    elif not isinstance(scan, HDF5TomoScan):
        raise ValueError(
            "Image key control only handle HDF5TomoScan and "
            "not {}".format(type(scan))
        )

    if "modifications" not in config:
        raise KeyError("modifications are not provided")
    else:
        modifications = config["modifications"]
        if modifications is None:
            modifications = {}

    image_keys_set = set(modifications.values())
    image_keys_set = set(
        [ImageKey.from_value(image_key) for image_key in image_keys_set]
    )
    for image_key_type in image_keys_set:
        frame_indexes_dict = dict(
            filter(lambda item: item[1] is image_key_type, modifications.items())
        )
        frame_indexes = tuple(frame_indexes_dict.keys())
        _logger.warning("will modify {} to {}".format(frame_indexes, image_key_type))
        _change_image_key_control(
            file_path=scan.master_file,
            entry=scan.entry,
            frames_indexes=frame_indexes,
            image_key_control_value=image_key_type.value,
            logger=_logger,
        )
    scan.clear_caches()
    scan._frames = None
    return scan


class ImageKeyEditor(SingleProcess):

    inputs = [
        _input_desc(
            name="data", type=TomwerScanBase, handler="pathReceived", doc="scan path"
        ),
    ]
    outputs = [_output_desc(name="data", type=TomwerScanBase, doc="scan path")]

    def process(self, scan=None):
        if scan is None:
            return None
        if not isinstance(scan, HDF5TomoScan):
            raise ValueError(
                "input type of {}: {} is not managed" "".format(scan, type(scan))
            )

        change_image_key_control(scan=scan, config=self.get_configuration())

        with scan.acquire_process_file_lock():
            self.register_process(
                process_file=scan.process_file,
                entry=scan.entry,
                configuration=self.get_configuration(),
                results={},
                process_index=scan.pop_process_index(),
                overwrite=True,
            )
        return scan

    @docstring(SingleProcess)
    def set_properties(self, properties):
        self.set_configuration(configuration=properties)

    @staticmethod
    def program_name():
        return "nxtomomill.utils.change_image_key_control"

    @staticmethod
    def program_version():
        return nxtomomill.version.version
