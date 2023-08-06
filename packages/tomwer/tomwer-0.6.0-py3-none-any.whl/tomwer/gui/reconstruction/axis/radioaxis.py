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
"""
contains gui relative to axis calculation using radios
"""

__authors__ = ["C. Nemoz", "H. Payno"]
__license__ = "MIT"
__date__ = "25/02/2019"

from silx.gui import qt
import logging
from tomwer.core.utils import image
import numpy
import enum
import os
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.synctools.axis import QAxisRP
from tomwer.core.process.reconstruction.axis.mode import AxisMode
from tomwer.core.process.reconstruction.axis.anglemode import CorAngleMode
from tomwer.core.process.reconstruction.axis.params import AxisCalculationInput
from tomoscan.scanbase import _FOV
import scipy.signal
from .CompareImages import CompareImages
from tomwer.gui.utils.buttons import PadlockButton
from silx.utils.deprecation import deprecated

_logger = logging.getLogger(__name__)


class RadioAxisWindow(qt.QMainWindow):
    """
    QMainWindow for defining the rotation axis

    .. snapshotqt:: img/AxisWindow.png

        from tomwer.gui.ftserie.axis import AxisWindow
        from tomwer.synctools.ftseries import QReconsParams
        import scipy.misc
        import scipy.ndimage

        recons_params = QReconsParams()
        widget = AxisWindow(recons_params)
        imgA = scipy.misc.ascent()
        imgB = scipy.ndimage.affine_transform(imgA, (1, 1), offset=(0, 10))

        widget.setImages(imgA=imgA, imgB=imgB, flipB=False)
        widget.show()

    :raises ValueError: given axis is not an instance of _QAxisRP
    """

    sigAxisEditionLocked = qt.Signal(bool)
    """Signal emitted when the status of the reconstruction parameters edition
    change"""

    sigLockModeChanged = qt.Signal(bool)
    """signal emitted when the lock on the mode change"""

    sigPositionChanged = qt.Signal(tuple)
    """signal emitted when the center of rotation center change"""

    def __init__(self, axis, parent=None):
        qt.QMainWindow.__init__(self, parent)
        if isinstance(axis, QAxisRP):
            self.__recons_params = axis
        else:
            raise TypeError("axis should be an instance of _QAxisRP")

        self._imgA = None
        self._imgB = None
        self._shiftedImgA = None
        self._flipB = True
        """Option if we want to flip the image B"""
        self.__callback = None
        self._scan = None
        self._axis_params = None
        self._lastManualFlip = None
        """Cache for the last user entry for manual flip"""
        self._lastXShift = None
        # cache to know if the x shift has changed since
        self._lastYShift = None
        # cache to know if the y shift has changed
        self._lastXOrigin = None
        # cache to know if the x origin has changed since
        self._lastYOrigin = None
        # cache to know if the y origin has changed since

        self.setWindowFlags(qt.Qt.Widget)
        self._plot = CompareImages(parent=self)
        self._plot.setAutoResetZoom(False)
        _mode = CompareImages.VisualizationMode.COMPOSITE_A_MINUS_B
        self._plot.setVisualizationMode(_mode)
        self.setCentralWidget(self._plot)

        self._dockWidgetCtrl = qt.QDockWidget(parent=self)
        self._dockWidgetCtrl.layout().setContentsMargins(0, 0, 0, 0)
        self._dockWidgetCtrl.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self._controlWidget = _AxisManual(
            parent=self, reconsParams=self.__recons_params
        )
        self._dockWidgetCtrl.setWidget(self._controlWidget)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self._dockWidgetCtrl)

        # expose API
        self.getXShift = self._controlWidget.getXShift
        self.getYShift = self._controlWidget.getYShift
        self._setShift = self._controlWidget.setShift
        self.setXShift = self._controlWidget.setXShift
        self.setYShift = self._controlWidget.setYShift
        self.getShiftStep = self._controlWidget.getShiftStep
        self.setShiftStep = self._controlWidget.setShiftStep
        self.getAxis = self._controlWidget.getAxis
        self.getMode = self._controlWidget.getMode
        self.setModeLock = self._controlWidget.setModeLock
        self.getEstimatedCor = self._controlWidget.getEstimatedCor

        # signal / slot connection
        self._controlWidget.sigShiftChanged.connect(self._updateShift)
        self._controlWidget.sigShiftChanged.connect(self._corChanged)
        self._controlWidget.sigRoiChanged.connect(self._updateShift)
        self._controlWidget.sigAuto.connect(self._updateAuto)
        self._controlWidget.sigModeChanged.connect(self.setMode)
        self._controlWidget.sigModeLockChanged.connect(self._modeLockChanged)
        self.__recons_params.sigChanged.connect(self._reset_scan)
        self._controlWidget.sigResetZoomRequested.connect(self._resetZoomPlot)
        self._controlWidget.sigSubsamplingChanged.connect(self._updateSubSampling)

        # adapt gui to the axis value
        self.setReconsParams(axis=self.__recons_params)

    def manual_uses_full_image(self, value):
        self._controlWidget.manual_uses_full_image(value)

    def _modeLockChanged(self, lock):
        self.sigLockModeChanged.emit(lock)

    def _corChanged(self):
        self.sigPositionChanged.emit((self.getXShift(), self.getYShift()))

    def getPlot(self):
        return self._plot

    def _resetZoomPlot(self):
        self._plot.getPlot().resetZoom()

    def getSettingsWidget(self):
        return self._controlWidget

    def setMode(self, mode):
        """
        Define the mode to use for radio axis

        :param mode:
        :return:
        """
        mode = AxisMode.from_value(mode)
        old_control = self._controlWidget.blockSignals(True)
        self._controlWidget.setMode(mode)
        self._controlWidget.blockSignals(old_control)

    def setEstimatedCor(self, value):
        self._controlWidget.setEstimatedCor(value=value)

    def getEstimatedCor(self):
        return self._controlWidget.getEstimatedCor()

    def _setModeLockFrmSettings(self, lock):
        # only lock the push button
        old = self.blockSignals(True)
        self._controlWidget._mainWidget._calculationWidget._lockMethodPB.setLock(lock)
        self.blockSignals(old)

    def getROIDims(self):
        if self.getMode() == AxisMode.manual:
            return self._controlWidget.getROIDims()
        else:
            return None

    def getROIOrigin(self):
        if self.getMode() == AxisMode.manual:
            return self._controlWidget.getROIOrigin()
        else:
            return None

    def getImgSubsampling(self):
        return self._controlWidget.getImgSubsampling()

    def _computationRequested(self):
        self.sigComputationRequested.emit()

    def setLocked(self, locked):
        old = self.blockSignals(True)
        if self._axis_params.mode not in (AxisMode.read, AxisMode.manual):
            self._axis_params.mode = AxisMode.manual
        self._controlWidget.setLocked(locked)
        self.blockSignals(old)
        self.sigAxisEditionLocked.emit(locked)

    def isModeLock(self):
        return self._controlWidget.isModeLock()

    def _validated(self):
        """callback when the validate button is activated"""
        self.sigApply.emit()

    def _setRadio2Flip(self, checked):
        self._plot.setRadio2Flip(checked)

    def _flipChanged(self, checked):
        if self.getMode() == AxisMode.manual:
            self._lastManualFlip = self._plot.isRadio2Flip()

        if checked == self._flipB:
            return
        else:
            self._flipB = checked
            self._updatePlot()

    def setReconsParams(self, axis):
        """

        :param AxisRP axis: axis to edit
        :return:
        """
        assert isinstance(axis, QAxisRP)
        self._axis_params = axis
        old = self.blockSignals(True)
        self.resetShift()
        self._controlWidget.setAxis(axis)
        self.blockSignals(old)

    def setScan(self, scan):
        """
        Update the interface concerning the given scan. Try to display the
        radios for angle 0 and 180.

        :param scan: scan for which we want the axis updated.
        :type scan: Union[str, tomwer.core.scan.TomoBase]
        """
        self.clear()
        _scan = scan
        if type(scan) is str:
            try:
                _scan = ScanFactory.create_scan_object(scan)
            except ValueError:
                raise ValueError("Fail to discover a valid scan in %s" % scan)
        elif not isinstance(_scan, TomwerScanBase):
            raise ValueError(
                "type of %s (%s) is invalid, scan should be a "
                "file/dir path or an instance of ScanBase" % (scan, type(scan))
            )
        assert isinstance(_scan, TomwerScanBase)

        if _scan.axis_params is None:
            _scan.axis_params = QAxisRP()

        if self._scan is not None:
            self._scan.axis_params.sigAxisUrlChanged.disconnect(self._updatePlot)
        if _scan.field_of_view == _FOV.HALF and self.getMode() is AxisMode.centered:
            _logger.info(
                "acquisition is half acquisition, switch algorithm "
                "for computing COR to centered"
            )
            self.setMode(AxisMode.global_)
            # might be added if near is finally added
            # if _scan.estimated_cor_frm_motor is not None:
            #     self.setEstimatedCor(_scan.estimated_cor_frm_motor)
        elif _scan.field_of_view == _FOV.FULL and self.getMode() is AxisMode.near:
            pass

        # update visualization
        self._scan = _scan
        self._scan.axis_params.sigAxisUrlChanged.connect(self._updatePlot)
        self._controlWidget.setScan(scan=self._scan)
        self._updatePlot()
        self.getPlot().getPlot().resetZoom()

    def _updatePlot(self):
        if self._scan is None:
            return
        old = self.blockSignals(True)
        coreAngleMode = CorAngleMode.from_value(self.__recons_params.angle_mode)
        axis_rp = self._scan.axis_params
        if coreAngleMode is CorAngleMode.manual_selection and axis_rp.n_url() == 2:
            pass
        else:
            res = self._scan.getRadiosForAxisCalc(mode=coreAngleMode)
            axis_rp.axis_url_1 = res[0]
            axis_rp.axis_url_2 = res[1]

        if axis_rp.n_url() < 2:
            _logger.error("Fail to detect radio for axis calculation")
        elif axis_rp.axis_url_1.url:
            # if necessary normalize data
            axis_rp.axis_url_1.normalize_data(self._scan, log_=False)
            axis_rp.axis_url_2.normalize_data(self._scan, log_=False)

            paganin = self.__recons_params.paganin_preproc
            # check if normed
            if paganin:
                imgA = axis_rp.axis_url_1.normalized_data_paganin
                imgB = axis_rp.axis_url_2.normalized_data_paganin
            else:
                imgA = axis_rp.axis_url_1.normalized_data
                imgB = axis_rp.axis_url_2.normalized_data
            assert imgA is not None
            assert imgB is not None
            self.setImages(imgA=imgA, imgB=imgB)
        else:
            _logger.error(
                "fail to find radios for angle 0 and 180. Unable to update axis gui"
            )
        self.blockSignals(old)

    def clear(self):
        if self._scan is not None:
            self._scan.axis_params.sigAxisUrlChanged.disconnect(self._updatePlot)
        self._scan = None

    def _reset_scan(self):
        if self._scan:
            self.setScan(scan=self._scan)

    def setImages(self, imgA, imgB):
        """

        :warning: does not reset the shift when change images

        :param numpy.array imgA: first image to compare. Will be the one shifted
        :param numpy.array imgB: second image to compare
        :param bool flipB: True if the image B has to be flipped
        :param bool paganin: True to apply paganin phase retrieval
        """
        assert imgA is not None
        assert imgB is not None
        _imgA = imgA
        _imgB = imgB

        if _imgA.shape != _imgB.shape:
            _logger.error(
                "The two provided images have incoherent shapes "
                "(%s vs %s)" % (_imgA.shape, _imgB.shape)
            )
        elif _imgA.ndim != 2:
            _logger.error("Image shape are not 2 dimensional")
        else:
            self._imgA = _imgA
            self._imgB = _imgB

            self._controlWidget._roiControl.setLimits(
                width=self._imgA.shape[1], height=self._imgA.shape[0]
            )
            self._updateShift()

    def _updateSubSampling(self):
        self._updateShift()
        self.getPlot().getPlot().resetZoom()

    def _updateShift(self, xShift=None, yShift=None):
        if self._imgA is None or self._imgB is None:
            return
        xShift = xShift or self.getXShift()
        yShift = yShift or self.getYShift()

        # TODO: we might avoid flipping image at each new x_shift...
        _imgA, _imgB = self._getRawImages()
        # apply shift
        if xShift == 0.0 and yShift == 0.0:
            self._shiftedImgA = _imgA
            self._shiftedImgB = _imgB
        else:
            try:
                # in fact the correct way would be to:
                # - shift image A of -x shift
                # - shift image B of +x shift
                # but it is faster to only shift image B of a factor 2* x shift
                self._shiftedImgA = image.shift_img(
                    data=_imgA,
                    dx=-self.getXShift() / self.getImgSubsampling(),
                    dy=self.getYShift() / self.getImgSubsampling(),
                    cval=_imgA.min(),
                )
                self._shiftedImgB = image.shift_img(
                    data=_imgB,
                    dx=self.getXShift() / self.getImgSubsampling(),
                    dy=self.getYShift() / self.getImgSubsampling(),
                    cval=_imgB.min(),
                )
            except ValueError as e:
                _logger.warning(e)
        old = self.blockSignals(True)
        self._plot.setData(image1=self._shiftedImgA, image2=self._shiftedImgB)
        roi_origin = self.getROIOrigin()
        if roi_origin is not None:
            x_origin, y_origin = roi_origin
        else:
            x_origin = y_origin = None
        self._lastXShift = xShift
        self._lastYShift = yShift
        self._lastXOrigin = x_origin
        self._lastYOrigin = y_origin
        self.blockSignals(old)

    def _getRawImages(self):
        def selectROI(data, width, height, x_origin, y_origin, subsampling):
            assert subsampling > 0
            x_min = x_origin - width // 2
            x_max = x_origin + width // 2
            y_min = y_origin - height // 2
            y_max = y_origin + height // 2
            return data[y_min:y_max:subsampling, x_min:x_max:subsampling]

        # get images and apply ROI if any
        _roi_dims = self.getROIDims()
        _origin = self.getROIOrigin()
        subsampling = self.getImgSubsampling()
        _imgA = self._imgA
        _imgB = self._imgB
        # flip image B
        _imgB = numpy.fliplr(_imgB)
        if _roi_dims is not None:
            assert type(_roi_dims) is tuple
            _imgA = selectROI(
                _imgA,
                width=_roi_dims[0],
                height=_roi_dims[1],
                x_origin=_origin[0],
                y_origin=_origin[1],
                subsampling=subsampling,
            )
            _imgB = selectROI(
                _imgB,
                width=_roi_dims[0],
                height=_roi_dims[1],
                x_origin=_origin[0],
                y_origin=_origin[1],
                subsampling=subsampling,
            )
        return _imgA, _imgB

    def _updateAuto(self):
        _imgA, _imgB = self._getRawImages()
        correlation = scipy.signal.correlate2d(in1=_imgA, in2=_imgB)
        y, x = numpy.unravel_index(numpy.argmax(correlation), correlation.shape)
        self._setShift(x=x, y=y)

    def resetShift(self):
        self._controlWidget.blockSignals(True)
        self._controlWidget.reset()
        self._controlWidget.blockSignals(False)
        if self._imgA and self._imgB:
            self.setImages(imgA=self._imgA, imgB=self._imgB)


class _AxisRead(qt.QWidget):
    """Widget to select a position value from a file"""

    sigFileChanged = qt.Signal(str)

    def __init__(self, parent, axis=None):
        qt.QWidget.__init__(self, parent)
        self._axis = None
        if axis:
            self.setAxis(axis)
        self.setLayout(qt.QHBoxLayout())

        self.layout().addWidget(qt.QLabel("File", parent=self))
        self._filePathQLE = qt.QLineEdit("", parent=self)
        self.layout().addWidget(self._filePathQLE)
        self._fileSelPB = qt.QPushButton("select", parent=self)
        self.layout().addWidget(self._fileSelPB)

        # connect signal / slot
        self._fileSelPB.pressed.connect(self._selectFile)
        self._filePathQLE.textChanged.connect(self._fileChanged)

    def setAxis(self, axis):
        assert isinstance(axis, QAxisRP)
        self._axis = axis

    def _selectFile(self):
        dialog = qt.QFileDialog(self)
        dialog.setFileMode(qt.QFileDialog.ExistingFile)

        if not dialog.exec_():
            dialog.close()
            return

        _file_path = dialog.selectedFiles()[0]
        _logger.info("user select file %s for reading position value" % _file_path)
        self._filePathQLE.setText(dialog.selectedFiles()[0])

    def _fileChanged(self, file_path):
        """callback when the line edit (containing the file path) changed"""
        if self._axis and os.path.isfile(file_path):
            self._axis.set_position_frm_par_file(file_path, force=True)


class _AxisManual(qt.QWidget):
    """
    Widget to define the shift to apply on an image
    """

    sigShiftChanged = qt.Signal(float, float)
    """Signal emitted when requested shift changed. Parameter is x, y"""

    sigModeLockChanged = qt.Signal(bool)
    """Signal emitted when the mode is lock or unlock"""

    sigResetZoomRequested = qt.Signal()
    """Signal emitted when request a zoom reset from the plot"""

    sigSubsamplingChanged = qt.Signal()
    """Signal emitted when subsampling change"""

    def __init__(self, parent, reconsParams):
        assert isinstance(reconsParams, QAxisRP)
        qt.QWidget.__init__(self, parent)
        self._xShift = 0
        self._yShift = 0
        self._recons_params = reconsParams or QAxisRP()
        self._axis = None

        self.setLayout(qt.QVBoxLayout())

        self._manualSelectionWidget = _AxisManualSelection(
            parent=self, shift_mode=ShiftMode.x_only
        )
        self._manualSelectionWidget.layout().setContentsMargins(0, 0, 0, 0)

        self._readFileSelWidget = _AxisRead(parent=self)
        self._readFileSelWidget.layout().setContentsMargins(0, 0, 0, 0)

        self._displacementSelector = self._manualSelectionWidget._displacementSelector
        self._shiftControl = self._manualSelectionWidget._shiftControl
        self._roiControl = self._manualSelectionWidget._roiControl
        self._imgOpts = self._manualSelectionWidget._imgOpts

        self._mainWidget = AxisTabWidget(
            parent=self,
            mode_dependant_widget=self._manualSelectionWidget,
            read_file_sel_widget=self._readFileSelWidget,
            recons_params=self._recons_params,
        )

        self.layout().addWidget(self._mainWidget)

        # signal / slot connection
        self._shiftControl.sigShiftLeft.connect(self._incrementLeftShift)
        self._shiftControl.sigShiftRight.connect(self._incrementRightShift)
        self._shiftControl.sigShiftTop.connect(self._incrementTopShift)
        self._shiftControl.sigShiftBottom.connect(self._incrementBottomShift)
        self._shiftControl.sigReset.connect(self._resetShift)
        self._shiftControl.sigShiftChanged.connect(self._setShiftAndSignal)
        self._mainWidget.sigLockModeChanged.connect(self._modeLockChanged)
        self._manualSelectionWidget.sigResetZoomRequested.connect(
            self._requestZoomReset
        )
        self._imgOpts.sigSubsamplingChanged.connect(self._subsamplingChanged)

        # expose API
        self.getShiftStep = self._displacementSelector.getShiftStep
        self.setShiftStep = self._displacementSelector.setShiftStep
        self.sigRoiChanged = self._roiControl.sigRoiChanged
        self.sigAuto = self._shiftControl.sigAuto
        self.getROIDims = self._roiControl.getROIDims
        self.getROIOrigin = self._roiControl.getROIOrigin
        self.getImgSubsampling = self._imgOpts.getSubsampling
        self.getMode = self._mainWidget.getMode
        self.sigModeChanged = self._mainWidget.sigModeChanged
        self.isModeLock = self._mainWidget.isModeLock
        self.setModeLock = self._mainWidget.setModeLock

        # set up interface
        self.setAxis(self._recons_params)

    def setScan(self, scan):
        self._mainWidget.setScan(scan=scan)
        self._roiControl.setScan(scan=scan)

    def manual_uses_full_image(self, value):
        self._roiControl.manual_uses_full_image(value)

    def _subsamplingChanged(self):
        self.sigSubsamplingChanged.emit()

    def _incrementLeftShift(self):
        self._incrementShift("left")

    def _incrementRightShift(self):
        self._incrementShift("right")

    def _incrementTopShift(self):
        self._incrementShift("top")

    def _incrementBottomShift(self):
        self._incrementShift("bottom")

    def _setShiftAndSignal(self, x, y):
        if x == self._xShift and y == self._yShift:
            return
        self.setShift(x, y)
        self._shiftControl._updateShiftInfo(x=x, y=y)
        self.sigShiftChanged.emit(x, y)

    def setAxis(self, axis):
        assert isinstance(axis, QAxisRP)
        old = self.blockSignals(True)
        if self._axis:
            self._axis.sigChanged.disconnect(self._updateAxisView)
        self._axis = axis
        self.setXShift(self._axis.value_ref_tomwer)
        self._mainWidget.setAxisParams(self._axis)
        self._readFileSelWidget.setAxis(self._axis)
        self._updateAxisView()
        self._axis.sigChanged.connect(self._updateAxisView)
        self.blockSignals(old)

    def _modeLockChanged(self, lock):
        self.sigModeLockChanged.emit(lock)

    def setMode(self, mode):
        self._axis.mode = mode
        self._updateAxisView()

    def setEstimatedCor(self, value):
        self._mainWidget.setEstimatedCorValue(value=value)

    def getEstimatedCor(self):
        return self._mainWidget.getEstimatedCor()

    def _updateAxisView(self):
        self._axis.blockSignals(True)
        if self._axis.value_ref_tomwer not in (None, "..."):
            self.setXShift(self._axis.value_ref_tomwer)
            # self._positionInfoWidget._updatePosition()
        self._axis.blockSignals(False)

        self._manualSelectionWidget.setVisible(self._axis.mode is AxisMode.manual)
        self._readFileSelWidget.setVisible(self._axis.mode is AxisMode.read)

    def getAxis(self):
        return self._axis

    def _incrementShift(self, direction):
        assert direction in ("left", "right", "top", "bottom")
        if direction == "left":
            self.setXShift(self._xShift - self.getShiftStep())
        elif direction == "right":
            self.setXShift(self._xShift + self.getShiftStep())
        elif direction == "top":
            self.setYShift(self._yShift + self.getShiftStep())
        else:
            self.setYShift(self._yShift - self.getShiftStep())

        self._shiftControl._updateShiftInfo(x=self._xShift, y=self._yShift)

    def _resetShift(self):
        old = self._axis.blockSignals(True)
        self.setXShift(0)
        self.setYShift(0)
        self._shiftControl._updateShiftInfo(x=self._xShift, y=self._yShift)
        self._axis.blockSignals(old)

        self.sigShiftChanged.emit(self._xShift, self._yShift)

    def getXShift(self):
        if self._xShift == "...":
            return 0
        return self._xShift

    def getYShift(self):
        if self._yShift == "...":
            return 0
        return self._yShift

    def setXShift(self, x: float):
        self.setShift(x=x, y=self._yShift)

    def setYShift(self, y):
        self.setShift(x=self._xShift, y=y)

    def setShift(self, x, y):
        if x == self._xShift and y == self._yShift:
            return
        self._xShift = x if x is not None else 0.0
        self._yShift = y if y is not None else 0.0
        if self._axis:
            old = self._axis.blockSignals(True)
            self._axis.set_value_ref_tomwer(x)
            self._axis.blockSignals(old)
        self._shiftControl._updateShiftInfo(x=self._xShift, y=self._yShift)
        self.sigShiftChanged.emit(self._xShift, self._yShift)

    def reset(self):
        self._xShift = 0
        self._yShift = 0
        self.sigShiftChanged.emit(self._xShift, self._yShift)

    def setLocked(self, locked):
        self._mainWidget.setEnabled(not locked)

    def _requestZoomReset(self):
        self.sigResetZoomRequested.emit()


class _AxisManualSelection(qt.QWidget):

    sigResetZoomRequested = qt.Signal()
    """Signal emitted when a zoom request is necessary (when change to full
    image)"""

    def __init__(self, parent, shift_mode):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        self._displacementSelector = _DisplacementSelector(parent=self)
        self.layout().addWidget(self._displacementSelector)

        self._shiftControl = _ShiftControl(parent=self, shift_mode=shift_mode)
        self.layout().addWidget(self._shiftControl)

        self._roiControl = _ROIControl(parent=self)
        self.layout().addWidget(self._roiControl)

        self._imgOpts = _ImgOpts(parent=self)
        self.layout().addWidget(self._imgOpts)

        # connect signal / slot
        self._roiControl.sigResetZoomRequested.connect(self._requestZoomReset)

    def _requestZoomReset(self):
        self.sigResetZoomRequested.emit()


class _ROIControl(qt.QGroupBox):
    """
    Widget used to define the ROI on images to compare
    """

    sigRoiChanged = qt.Signal(object)
    """Signal emitted when the ROI changed"""
    sigResetZoomRequested = qt.Signal()
    """Signal emitted when a zoom request is necessary (when change to full
    image)"""

    def __init__(self, parent):
        qt.QGroupBox.__init__(self, "ROI selection", parent)
        self.setLayout(qt.QVBoxLayout())

        self._buttonGrp = qt.QButtonGroup(parent=self)
        self._buttonGrp.setExclusive(True)

        self._roiWidget = qt.QWidget(parent=self)
        self._roiWidget.setLayout(qt.QHBoxLayout())
        self._roiWidget.layout().setContentsMargins(0, 0, 0, 0)
        self._roiButton = qt.QRadioButton("ROI", parent=self._roiWidget)
        self._roiWidget.layout().addWidget(self._roiButton)
        self._buttonGrp.addButton(self._roiButton)
        self._roiDefinition = _ROIDefinition(parent=self)
        self._roiWidget.layout().addWidget(self._roiDefinition)
        self.layout().addWidget(self._roiWidget)

        self._fullImgButton = qt.QRadioButton("full image", parent=self)
        self._buttonGrp.addButton(self._fullImgButton)
        self.layout().addWidget(self._fullImgButton)

        # connect signal / Slot
        self._roiButton.toggled.connect(self._roiDefinition.setEnabled)
        self._fullImgButton.toggled.connect(self._requestZoomReset)

        # expose API
        self.sigRoiChanged = self._roiDefinition.sigRoiChanged
        self.getROIDims = self._roiDefinition.getROIDims
        self.getROIOrigin = self._roiDefinition.getROIOrigin
        self.setLimits = self._roiDefinition.setLimits
        self.setScan = self._roiDefinition.setScan

        # setup for full image
        self._roiButton.setChecked(True)

    def manual_uses_full_image(self, activate):
        if activate:
            self._fullImgButton.setChecked(True)
        else:
            self._roiButton.setChecked(True)

    def _requestZoomReset(self):
        self.sigResetZoomRequested.emit()


class _ROIDefinition(qt.QWidget):
    """
    Widget used to define ROI width and height.

    :note: emit ROI == None if setDisabled
    """

    sigRoiChanged = qt.Signal(object)
    """Signal emitted when the ROI changed"""

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())
        self._already_set = False

        # width & height
        self.layout().addWidget(qt.QLabel("dims", self), 0, 0)
        self._widthSB = qt.QSpinBox(parent=self)
        self._widthSB.setSingleStep(2)
        self._widthSB.setMaximum(10000)
        self._widthSB.setSuffix(" px")
        self._widthSB.setPrefix("w: ")
        self._widthSB.setToolTip("ROI width")
        self.layout().addWidget(self._widthSB, 0, 1)
        self._heightSB = qt.QSpinBox(parent=self)
        self._heightSB.setSingleStep(2)
        self._heightSB.setSuffix(" px")
        self._heightSB.setPrefix("h: ")
        self._heightSB.setToolTip("ROI height")
        self._heightSB.setMaximum(10000)
        self.layout().addWidget(self._heightSB, 0, 2)

        # origin x and y position
        self.layout().addWidget(qt.QLabel("origin", self), 1, 0)
        self._xOriginSB = qt.QSpinBox(parent=self)
        self._xOriginSB.setSingleStep(10)
        self._xOriginSB.setMaximum(10000)
        self._xOriginSB.setPrefix("x: ")
        self.layout().addWidget(self._xOriginSB, 1, 1)
        self._yOriginSB = qt.QSpinBox(parent=self)
        self._yOriginSB.setSingleStep(10)
        self._yOriginSB.setPrefix("y: ")
        self._yOriginSB.setMaximum(10000)
        self.layout().addWidget(self._yOriginSB, 1, 2)

        # Signal / Slot connection
        self._widthSB.editingFinished.connect(self.__roiChanged)
        self._heightSB.editingFinished.connect(self.__roiChanged)
        self._xOriginSB.editingFinished.connect(self.__roiChanged)
        self._yOriginSB.editingFinished.connect(self.__roiChanged)

    def __roiChanged(self, *args, **kwargs):
        self.sigRoiChanged.emit((self.getROIDims(), self.getROIOrigin()))

    def setLimits(self, width, height):
        """

        :param int x: width maximum value
        :param int height: height maximum value
        """
        for spinButton in (self._widthSB, self._heightSB):
            spinButton.blockSignals(True)
        assert type(width) is int
        assert type(height) is int
        valueChanged = False
        if self._widthSB.value() > width:
            self._widthSB.setValue(width)
            valueChanged = True
        if self._heightSB.value() > height:
            self._heightSB.setValue(height)
            valueChanged = True

        # if this is the first limit definition, propose default width and
        # height
        if self._widthSB.value() == 0:
            self._widthSB.setValue(min(256, width))
            valueChanged = True
        if self._heightSB.value() == 0:
            self._heightSB.setValue(min(256, height))
            valueChanged = True

        # define minimum / maximum
        self._widthSB.setRange(1, width)
        self._heightSB.setRange(1, height)
        for spinButton in (self._widthSB, self._heightSB):
            spinButton.blockSignals(False)
        if valueChanged is True:
            self.__roiChanged()

    def getROIDims(self):
        """

        :return: (width, height) or None
        :rtype: Union[None, tuple]
        """
        if self.isEnabled():
            return (self._widthSB.value(), self._heightSB.value())
        else:
            return None

    def getROIOrigin(self):
        if self.isEnabled():
            return (self._xOriginSB.value(), self._yOriginSB.value())
        else:
            return None

    def setEnabled(self, *arg, **kwargs):
        qt.QWidget.setEnabled(self, *arg, **kwargs)
        self.__roiChanged()

    def setScan(self, scan):
        if not self._already_set:
            self._already_set = True
            x_origin = scan.dim_1 // 2
            y_origin = scan.dim_2 // 2
            self._xOriginSB.setValue(x_origin)
            self._yOriginSB.setValue(y_origin)


@enum.unique
class ShiftMode(enum.Enum):
    x_only = 0
    y_only = 1
    x_and_y = 2


class _ShiftControl(qt.QWidget):
    """
    Widget to control the shift step we want to apply
    """

    sigShiftLeft = qt.Signal()
    """Signal emitted when the left button is activated"""
    sigShiftRight = qt.Signal()
    """Signal emitted when the right button is activated"""
    sigShiftTop = qt.Signal()
    """Signal emitted when the top button is activated"""
    sigShiftBottom = qt.Signal()
    """Signal emitted when the bottom button is activated"""
    sigReset = qt.Signal()
    """Signal emitted when the reset button is activated"""
    sigAuto = qt.Signal()
    """Signal emitted when the auto button is activated"""
    sigShiftChanged = qt.Signal(float, float)
    """Signal emitted ony when xLE and yLE edition is finished"""

    def __init__(self, parent, shift_mode):
        """

        :param parent: qt.QWidget
        :param ShiftMode shift_mode: what are the shift we want to control
        """
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self._leftButton = qt.QPushButton("left", parent=self)
        self.layout().addWidget(self._leftButton, 1, 0)

        self._rightButton = qt.QPushButton("right", parent=self)
        self.layout().addWidget(self._rightButton, 1, 3)

        self._shiftInfo = _ShiftInformation(parent=self)
        self.layout().addWidget(self._shiftInfo, 1, 1)
        self._shiftInfo._updateShiftInfo(x=0.0, y=0.0)

        self._topButton = qt.QPushButton("top", parent=self)
        self.layout().addWidget(self._topButton, 0, 1)

        self._bottomButton = qt.QPushButton("bottom", parent=self)
        self.layout().addWidget(self._bottomButton, 2, 1)

        self._resetButton = qt.QPushButton("reset", parent=self)
        self.layout().addWidget(self._resetButton, 3, 2, 3, 4)

        self._autoButton = qt.QPushButton("auto", parent=self)
        self.layout().addWidget(self._autoButton, 3, 0, 3, 2)
        self._autoButton.hide()

        # Signal / Slot connection
        self._leftButton.pressed.connect(self.sigShiftLeft.emit)
        self._rightButton.pressed.connect(self.sigShiftRight.emit)
        self._topButton.pressed.connect(self.sigShiftTop.emit)
        self._bottomButton.pressed.connect(self.sigShiftBottom.emit)
        self._resetButton.pressed.connect(self.sigReset.emit)
        self._autoButton.pressed.connect(self.sigAuto.emit)
        self._shiftInfo.sigShiftChanged.connect(self.sigShiftChanged.emit)

        # expose API
        self._updateShiftInfo = self._shiftInfo._updateShiftInfo

        self.setShiftMode(shift_mode)

    def setShiftMode(self, shift_mode):
        show_x_shift = shift_mode in (ShiftMode.x_only, ShiftMode.x_and_y)
        show_y_shift = shift_mode in (ShiftMode.y_only, ShiftMode.x_and_y)
        self._leftButton.setVisible(show_x_shift)
        self._rightButton.setVisible(show_x_shift)
        self._topButton.setVisible(show_y_shift)
        self._bottomButton.setVisible(show_y_shift)
        self._shiftInfo._xLE.setVisible(show_x_shift)
        self._shiftInfo._xLabel.setVisible(show_x_shift)
        self._shiftInfo._yLE.setVisible(show_y_shift)
        self._shiftInfo._yLabel.setVisible(show_y_shift)


class _ImgOpts(qt.QGroupBox):

    sigSubsamplingChanged = qt.Signal()
    """Signal emitted when the subsampling change"""

    def __init__(self, parent, title="Image Option"):
        super().__init__(title, parent)
        self.setLayout(qt.QFormLayout())
        self._subsamplingQSpinBox = qt.QSpinBox(self)
        self.layout().addRow("subsampling:", self._subsamplingQSpinBox)
        self._subsamplingQSpinBox.setMinimum(1)

        # set up
        self._subsamplingQSpinBox.setValue(1)

        # connect signal / slot
        self._subsamplingQSpinBox.valueChanged.connect(self._subsamplingChanged)

    def _subsamplingChanged(self):
        self.sigSubsamplingChanged.emit()

    def getSubsampling(self):
        return self._subsamplingQSpinBox.value()

    def setSubsampling(self, value):
        return self._subsamplingQSpinBox.setValue(int(value))


class _ShiftInformation(qt.QWidget):
    """
    Widget displaying information about the current x and y shift.
    Both x shift and y shift are editable.
    """

    class _ShiftLineEdit(qt.QLineEdit):
        def __init__(self, *args, **kwargs):
            qt.QLineEdit.__init__(self, *args, **kwargs)
            validator = qt.QDoubleValidator(parent=self, decimals=2)
            self.setValidator(validator)

        def sizeHint(self):
            return qt.QSize(40, 10)

    sigShiftChanged = qt.Signal(float, float)
    """Signal emitted ony when xLE and yLE edition is finished"""

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self._xLabel = qt.QLabel("x=", parent=self)
        self.layout().addWidget(self._xLabel)
        self._xLE = _ShiftInformation._ShiftLineEdit("", parent=self)
        self.layout().addWidget(self._xLE)

        self._yLabel = qt.QLabel("y=", parent=self)
        self.layout().addWidget(self._yLabel)
        self._yLE = _ShiftInformation._ShiftLineEdit("", parent=self)
        self.layout().addWidget(self._yLE)

        # connect Signal / Slot
        self._xLE.editingFinished.connect(self._shiftChanged)
        self._yLE.editingFinished.connect(self._shiftChanged)

    def _updateShiftInfo(self, x, y):
        self.blockSignals(True)
        if x is None:
            x = 0.0
        if y is None:
            y = 0.0
        x_text = x
        if x_text != "...":
            x_text = "%.1f" % float(x)
        y_text = y
        if y_text != "...":
            y_text = "%.1f" % float(y)
        self._xLE.setText(x_text)
        self._yLE.setText(y_text)
        self.blockSignals(False)

    def _shiftChanged(self, *args, **kwargs):
        self.sigShiftChanged.emit(float(self._xLE.text()), float(self._yLE.text()))


class _DisplacementSelector(qt.QGroupBox):
    """
    Group box to define the displacement step value
    """

    def __init__(self, parent):
        qt.QGroupBox.__init__(self, "shift step", parent)
        self.setLayout(qt.QVBoxLayout())
        self._buttonGrp = qt.QButtonGroup(parent=self)
        self._buttonGrp.setExclusive(True)

        self._rawButton = qt.QRadioButton("Raw (1 pixel)", parent=self)
        self.layout().addWidget(self._rawButton)
        self._buttonGrp.addButton(self._rawButton)

        self._fineButton = qt.QRadioButton("Fine (0.1 pixel)", parent=self)
        self.layout().addWidget(self._fineButton)
        self._buttonGrp.addButton(self._fineButton)

        self._manualWidget = qt.QWidget(parent=self)
        self._manualWidget.setLayout(qt.QHBoxLayout())
        self._manualWidget.layout().setContentsMargins(0, 0, 0, 0)
        self._manualWidget.layout().setSpacing(0)
        self._manualButton = qt.QRadioButton("Manual", parent=self._manualWidget)
        self._manualWidget.layout().addWidget(self._manualButton)
        self._manualLE = qt.QLineEdit("0.5", parent=self._manualWidget)
        validator = qt.QDoubleValidator(parent=self._manualLE, decimals=2)
        validator.setBottom(0.0)
        self._manualLE.setValidator(validator)
        self._manualWidget.layout().addWidget(self._manualLE)

        self.layout().addWidget(self._manualWidget)
        self._manualLE.setEnabled(False)
        self._buttonGrp.addButton(self._manualButton)

        self._rawButton.setChecked(True)

        # signal / slot connection
        self._manualButton.toggled.connect(self._manualLE.setEnabled)

    def getShiftStep(self):
        """

        :return: displacement shift defined
        :rtype: float
        """
        if self._rawButton.isChecked():
            return 1.0
        elif self._fineButton.isChecked():
            return 0.1
        else:
            return float(self._manualLE.text())

    def setShiftStep(self, value):
        """

        :param float value: shift step
        """
        assert type(value) is float
        self._manualButton.setChecked(True)
        self._manualLE.setText(str(value))


class _AxisOptionsWidget(qt.QWidget):
    """GUI to tune the axis algorithm"""

    def __init__(self, parent, axis):
        qt.QWidget.__init__(self, parent=parent)
        assert isinstance(axis, QAxisRP)
        self._axis = axis
        self.setLayout(qt.QVBoxLayout())

        # define common options
        self._commonOpts = qt.QWidget(parent=self)
        self._commonOpts.setLayout(qt.QFormLayout())

        self._qcbDataMode = qt.QComboBox(parent=self)
        for data_mode in AxisCalculationInput:
            # paganin is not managed for sinogram
            self._qcbDataMode.addItem(data_mode.name(), data_mode)
        # for now not handle
        # self._commonOpts.layout().addRow('data mode', self._qcbDataMode)
        self._qcbDataMode.hide()

        # add scale option
        self._scaleOpt = qt.QCheckBox(parent=self)
        self._commonOpts.layout().addRow("scale the two images", self._scaleOpt)
        self.layout().addWidget(self._commonOpts)

        # add option for computing min-max
        # TODO
        pass

        # add near options
        self._nearOpts = _AxisNearOptsWidget(parent=self, axis=self._axis)
        self.layout().addWidget(self._nearOpts)

        # set up
        self.setCalculationInputType(self._axis.calculation_input_type)

        # connect signal / slot
        self._scaleOpt.toggled.connect(self._updateScaleOpt)
        self._qcbDataMode.currentIndexChanged.connect(self._updateInputType)
        self._axis.sigChanged.connect(self._updateMode)

    def setMode(self, mode):
        mode_ = AxisMode.from_value(mode)
        self._nearOpts.setVisible(mode_ == AxisMode.near)

    def _updateMode(self):
        old = self.blockSignals(True)
        self._nearOpts.setVisible(self._axis.mode == AxisMode.near)
        index = self._qcbDataMode.findText(self._axis.calculation_input_type.name())
        if index >= 0:
            self._qcbDataMode.setCurrentIndex(index)
        self.blockSignals(old)

    def _updateScaleOpt(self, *arg, **kwargs):
        self._axis.scale_img2_to_img1 = self.isImageScaled()

    def isImageScaled(self):
        return self._scaleOpt.isChecked()

    def _updateInputType(self, *arg, **kwargs):
        self._axis.calculation_input_type = self.getCalulationInputType()

    def getCalulationInputType(self, *arg, **kwargs):
        return AxisCalculationInput.from_value(self._qcbDataMode.currentText())

    def setCalculationInputType(self, calculation_type):
        calculation_type = AxisCalculationInput.from_value(calculation_type)
        index_dm = self._qcbDataMode.findText(calculation_type.name())
        self._qcbDataMode.setCurrentIndex(index_dm)

    def setAxisParams(self, axis):
        self._nearOpts.setAxisParams(axis=axis)
        self._axis = axis
        old = self.blockSignals(True)
        self._scaleOpt.setChecked(axis.scale_img2_to_img1)
        index = self._qcbDataMode.findText(axis.calculation_input_type.name())
        self._qcbDataMode.setCurrentIndex(index)
        self.blockSignals(old)


class _AxisNearOptsWidget(qt.QWidget):
    """GUI dedicated to the neat option"""

    def __init__(self, parent, axis):
        qt.QWidget.__init__(self, parent=parent)
        assert isinstance(axis, QAxisRP)
        self._axis = axis

        self.setLayout(qt.QFormLayout())

        self._stdMaxOpt = qt.QCheckBox(parent=self)
        self.layout().addRow("look at max standard deviation", self._stdMaxOpt)

        self._nearWX = qt.QSpinBox(parent=self)
        self._nearWX.setMinimum(1)
        self._nearWX.setValue(5)
        self.layout().addRow("window size", self._nearWX)

        self._fineStepX = qt.QDoubleSpinBox(parent=self)
        self._fineStepX.setMinimum(0.05)
        self._fineStepX.setSingleStep(0.05)
        self._fineStepX.setMaximum(1.0)
        self.layout().addRow("fine step x", self._fineStepX)

        # connect signal / Slot
        self._stdMaxOpt.toggled.connect(self._lookforStxMaxChanged)
        self._nearWX.valueChanged.connect(self._windowSizeChanged)
        self._fineStepX.valueChanged.connect(self._fineStepXChanged)

    def _lookforStxMaxChanged(self, *args, **kwargs):
        self._axis.look_at_stdmax = self.isLookAtStdMax()

    def isLookAtStdMax(self):
        """

        :return: is the option for looking at max standard deviation is
                 activated
        :rtype: bool
        """
        return self._stdMaxOpt.isChecked()

    def _windowSizeChanged(self, *args, **kwargs):
        self._axis.near_wx = self.getWindowSize()

    def getWindowSize(self):
        """

        :return: window size for near search
        :rtype: int
        """
        return self._nearWX.value()

    def _fineStepXChanged(self, *args, **kwargs):
        self._axis.fine_step_x = self.getFineStepX()

    def getFineStepX(self):
        """

        :return: fine step x for near calculation
        :rtype: float
        """
        return self._fineStepX.value()

    def setAxisParams(self, axis):
        """

        :param axis: axis to edit
        :type: AxisRP
        """
        old = self.blockSignals(True)
        self._axis = axis
        self._stdMaxOpt.setChecked(axis.look_at_stdmax)
        self._nearWX.setValue(axis.near_wx)
        self._fineStepX.setValue(axis.fine_step_x)
        self.blockSignals(old)


class AxisTabWidget(qt.QTabWidget):
    """
    TabWidget containing all the information to edit the AXIS parameters
    """

    sigLockModeChanged = qt.Signal(bool)
    """signal emitted when the mode lock change"""

    def __init__(
        self,
        recons_params,
        parent=None,
        mode_dependant_widget=None,
        read_file_sel_widget=None,
    ):
        """

        :param recons_params: reconstruction parameters edited by the widget
        :type: QAxisRP
        :param mode_dependant_widget: widget used for manual selection of the
                                      axis
        :type mode_dependant_widget: Union[None, `._AxisManualSelection`]
        :param read_file_sel_widget: widget used to select a par file containing
                                     the axis position
        :type read_file_sel_widget: Union[None, `._AxisRead`]
        """
        qt.QTabWidget.__init__(self, parent)
        assert recons_params is not None
        # first tab 'calculation widget'
        self._calculationWidget = _CalculationWidget(
            parent=self, axis_params=recons_params
        )

        # second tab: options
        self._optionsWidget = _AxisOptionsWidget(parent=self, axis=recons_params)
        self._inputWidget = _InputWidget(parent=self, axis_params=recons_params)

        if mode_dependant_widget:
            self._calculationWidget.layout().addWidget(mode_dependant_widget)

        if read_file_sel_widget:
            self._calculationWidget.layout().addWidget(read_file_sel_widget)

        for widget in self._calculationWidget, self._optionsWidget:
            spacer = qt.QWidget(self)
            spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
            widget.layout().addWidget(spacer)

        self._optionsSA = qt.QScrollArea(parent=self)
        self._optionsSA.setWidget(self._optionsWidget)
        self.addTab(self._calculationWidget, "calculation")
        self.addTab(self._optionsSA, "options")
        self.addTab(self._inputWidget, "input")

        self.setAxisParams(recons_params)
        # set up
        self._optionsWidget.setMode(self.getMode())

        # expose API
        self.sigModeChanged = self._calculationWidget.sigModeChanged
        self.isModeLock = self._calculationWidget.isModeLock
        self.setModeLock = self._calculationWidget.setModeLock
        self.setEstimatedCorValue = self._calculationWidget.setEstimatedCorValue
        self.getEstimatedCor = self._calculationWidget.getEstimatedCor

        # connect signal / slot
        self._calculationWidget.sigLockModeChanged.connect(
            self._propagateSigLockModeChanged
        )

    def _propagateSigLockModeChanged(self, lock):
        self.sigLockModeChanged.emit(lock)

    def getMode(self):
        """Return algorithm to use for axis calculation"""
        return self._calculationWidget.getMode()

    def setScan(self, scan):
        if scan is not None:
            self._inputWidget.setScanRange(scan.scan_range)

    def setAxisParams(self, axis):
        old = self.blockSignals(True)
        self._calculationWidget.setAxisParams(axis)
        self._optionsWidget.setAxisParams(axis)
        self._inputWidget.setAxisParams(axis)
        self.blockSignals(old)


class _CalculationWidget(qt.QWidget):
    """Main widget to select the algorithm to use for COR calculation"""

    sigModeChanged = qt.Signal(str)
    """signal emitted when the algorithm for computing COR changed"""

    sigLockModeChanged = qt.Signal(bool)
    """signal emitted when the mode has been lock or unlock"""

    def __init__(self, parent, axis_params):
        assert isinstance(axis_params, QAxisRP)
        qt.QWidget.__init__(self, parent)
        self._axis_params = None
        self.setLayout(qt.QVBoxLayout())

        self._modeWidget = qt.QWidget(parent=self)
        self._modeWidget.setLayout(qt.QHBoxLayout())
        self.layout().addWidget(self._modeWidget)

        self.__rotAxisSelLabel = qt.QLabel("algorithm to compute cor")
        self._modeWidget.layout().addWidget(self.__rotAxisSelLabel)
        self._qcbPosition = qt.QComboBox(self)
        # add centered value
        self._qcbPosition.addItem(AxisMode.centered.value)
        idx = self._qcbPosition.findText(AxisMode.centered.value)
        global_tooltip = 'Dedicated to fullfield. Previously named "accurate"'
        self._qcbPosition.setItemData(idx, global_tooltip, qt.Qt.ToolTipRole)
        # add global value
        self._qcbPosition.addItem(AxisMode.global_.value)
        idx = self._qcbPosition.findText(AxisMode.global_.value)
        global_tooltip = (
            "Algorithm which can work for both half acquisition"
            " and standard ('full field') acquisition"
        )
        self._qcbPosition.setItemData(idx, global_tooltip, qt.Qt.ToolTipRole)
        # add sliding window value
        self._qcbPosition.addItem(AxisMode.sliding_window.value)
        idx = self._qcbPosition.findText(AxisMode.sliding_window.value)
        sliding_w_tooltip = (
            "A method for estimating semi-automatically the CoR position. "
            "You have to provide a hint on where the CoR is "
            "(left, center, right). Also works for sinograms."
        )
        self._qcbPosition.setItemData(idx, sliding_w_tooltip, qt.Qt.ToolTipRole)
        # add growing window value
        self._qcbPosition.addItem(AxisMode.growing_window.value)
        idx = self._qcbPosition.findText(AxisMode.growing_window.value)
        growing_w_tooltip = "A auto-Cor method also working for sinograms."
        self._qcbPosition.setItemData(idx, growing_w_tooltip, qt.Qt.ToolTipRole)
        # self._qcbPosition.addItem(AxisMode.near.value)
        # add manual
        self._qcbPosition.addItem(AxisMode.manual.value)
        # add read value
        self._qcbPosition.addItem(AxisMode.read.value)

        # add tooltips
        def add_tooltip(value, tooltip):
            idx = self._qcbPosition.findText(value)
            self._qcbPosition.setItemData(idx, tooltip, qt.Qt.ToolTipRole)

        # centered tooltip
        tooltip = "Default algorithm to compute COR from full field acquisition"
        add_tooltip(value=AxisMode.centered.value, tooltip=tooltip)
        # near tooltip
        tooltip = "Default algorithm to compute COR from half field acquisition"
        add_tooltip(value=AxisMode.near.value, tooltip=tooltip)
        # manual tooltip
        tooltip = "Enter manually the COR value"
        add_tooltip(value=AxisMode.manual.value, tooltip=tooltip)
        # read tooltip
        tooltip = "Read COR value from a file"
        add_tooltip(value=AxisMode.read.value, tooltip=tooltip)

        self._modeWidget.layout().addWidget(self._qcbPosition)

        # method lock button
        self._lockMethodPB = PadlockButton(parent=self._modeWidget)
        self._lockMethodPB.setToolTip(
            "Lock the method to compute the cor. \n"
            "This will automatically call the "
            "defined algorithm each time a scan is received."
        )
        self._modeWidget.layout().addWidget(self._lockMethodPB)

        self._optsWidget = qt.QWidget(self)
        self._optsWidget.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self._optsWidget)

        # padding option
        self._padding_widget = qt.QGroupBox("padding mode")
        self._padding_widget.setCheckable(True)
        self._optsWidget.layout().addWidget(self._padding_widget)
        self._padding_widget.setLayout(qt.QHBoxLayout())

        self._qbPaddingMode = qt.QComboBox(self._padding_widget)
        for _mode in (
            "constant",
            "edge",
            "linear_ramp",
            "maximum",
            "mean",
            "median",
            "minimum",
            "reflect",
            "symmetric",
            "wrap",
        ):
            self._qbPaddingMode.addItem(_mode)

        self._padding_widget.layout().addWidget(self._qbPaddingMode)

        # side option
        self._sideWidget = qt.QWidget(self)
        self._sideWidget.setLayout(qt.QHBoxLayout())
        self._optsWidget.layout().addWidget(self._sideWidget)
        self._sideWidget.layout().addWidget(qt.QLabel("side:", self))
        self._sideCB = qt.QComboBox(self._optsWidget)
        self._sideWidget.layout().addWidget(self._sideCB)
        self._sideCB.setToolTip(
            "Define a side for the sliding and growing" "window algorithms"
        )

        # near mode options
        self._nearOptsWidget = qt.QWidget(parent=self)
        self._nearOptsWidget.setLayout(qt.QVBoxLayout())
        self._optsWidget.layout().addWidget(self._nearOptsWidget)

        #    near value lock button
        self._nearValueCB = qt.QCheckBox("Overwrite estimated value")
        self._nearValueCB.setToolTip(
            "If the acquisition contains an "
            "estimation of the COR value then "
            "will set it automatically as estimated "
            "value."
        )
        self._nearOptsWidget.layout().addWidget(self._nearValueCB)
        self._nearOptsWidget.hide()

        #    LineEdit position value
        self._qleValueW = qt.QWidget(self._nearOptsWidget)
        self._qleValueW.setLayout(qt.QFormLayout())
        self._nearOptsWidget.layout().addWidget(self._qleValueW)

        self._qleNearPosQLE = qt.QLineEdit("0", self._nearOptsWidget)
        validator = qt.QDoubleValidator(self._qleNearPosQLE)
        self._qleNearPosQLE.setValidator(validator)
        self._qleValueW.layout().addRow("estimated value:", self._qleNearPosQLE)

        # connect signal / slot
        self._qcbPosition.currentIndexChanged.connect(self._modeChanged)
        self._qleNearPosQLE.editingFinished.connect(self._nearValueChanged)
        self._sideCB.currentTextChanged.connect(self._sideChanged)
        self._lockMethodPB.sigLockChanged.connect(self.lockMode)
        self._qbPaddingMode.currentIndexChanged.connect(self._paddingModeChanged)
        self._padding_widget.toggled.connect(self._paddingModeChanged)

        # set up interface
        self._sideWidget.setVisible(False)
        self.setAxisParams(axis_params)
        self._nearValueCB.setChecked(True)

    def setEstimatedCorValue(self, value):
        if value is not None:
            self._qleNearPosQLE.setText(str(value))

    def getEstimatedCor(self):
        return float(self._qleNearPosQLE.text())

    def nearValueIsLocked(self):
        return not self._nearValueCB.isChecked()

    def setSide(self, side):
        if side is not None:
            idx = self._sideCB.findText(side)
            if idx >= 0:
                self._sideCB.setCurrentIndex(idx)

    def getSide(self):
        return self._sideCB.currentText()

    def _modeChanged(self, *args, **kwargs):
        self._qleNearPosQLE.setVisible(self.getMode() == AxisMode.near)
        self._padding_widget.setVisible(
            self.getMode()
            in (
                AxisMode.centered,
                AxisMode.global_,
                AxisMode.growing_window,
                AxisMode.sliding_window,
            )
        )
        if self.getMode() in (
            AxisMode.near,
            AxisMode.centered,
            AxisMode.global_,
            AxisMode.growing_window,
            AxisMode.sliding_window,
        ):
            self._lockMethodPB.setVisible(True)
        else:
            self._lockMethodPB.setVisible(False)
            self.lockMode(False)

        side_visible = self.getMode() in (
            AxisMode.growing_window,
            AxisMode.sliding_window,
        )
        self._sideWidget.setVisible(side_visible)
        if side_visible is True:
            self._updateSideVisible(mode=self.getMode())

        self.sigModeChanged.emit(self.getMode().value)

    def _updateSideVisible(self, mode: AxisMode):
        if mode not in (AxisMode.growing_window, AxisMode.sliding_window):
            return
        else:
            current_value = self._axis_params.side
            old = self._sideCB.blockSignals(True)
            self._sideCB.clear()
            values = ["left", "right", "center"]
            if mode is AxisMode.growing_window:
                values.append("all")
            for value in values:
                self._sideCB.addItem(value)
            idx = self._sideCB.findText(current_value)
            print()
            if idx >= 0:
                self._sideCB.setCurrentIndex(idx)
            self._sideCB.blockSignals(old)
            self._axis_params.side = self.getSide()

    def isModeLock(self):
        return self._lockMethodPB.isLocked()

    def setModeLock(self, mode=None):
        """set a specific mode and lock it.

        :param mode: mode to lock. If None then keep the current mode
        """
        if mode is not None:
            mode = AxisMode.from_value(mode)
        if mode is None and self.getMode() not in (
            AxisMode.centered,
            AxisMode.near,
            AxisMode.global_,
        ):
            raise ValueError(
                "Unable to lock the current mode is not an automatic algorithm"
            )
        elif mode != self.getMode() and mode not in (
            AxisMode.centered,
            AxisMode.near,
            AxisMode.global_,
        ):
            raise ValueError("Unable to lock %s this is not a lockable mode")

        if mode is not None:
            self.setMode(mode)
        if not self._lockMethodPB.isLocked():
            old = self._lockMethodPB.blockSignals(True)
            self._lockMethodPB.setLock(True)
            self._lockMethodPB.blockSignals(old)
        self.lockMode(True)

    def lockMode(self, lock):
        old = self._lockMethodPB.blockSignals(True)
        self._lockMethodPB.setLock(lock)
        for widget in (self._qcbPosition, self._qleNearPosQLE):
            widget.setEnabled(not lock)
        self._lockMethodPB.blockSignals(old)
        self.sigLockModeChanged.emit(lock)

    def getMode(self):
        """Return algorithm to use for axis calculation"""
        return AxisMode.from_value(self._qcbPosition.currentText())

    def setMode(self, mode):
        index = self._qcbPosition.findText(mode.value)
        if index >= 0:
            self._qcbPosition.setCurrentIndex(index)

    def _nearValueChanged(self, *args, **kwargs):
        self._axis_params.estimated_cor = self.getEstimatedCor()

    @deprecated(replacement="getEstimatedCor", since_version="0.6")
    def getNearPosition(self):
        return self.getEstimatedCor()

    @deprecated(replacement="setEstimatedCorValue", since_version="0.6")
    def setNearPosition(self, position):
        self.setEstimatedCorValue(position)

    def _paddingModeChanged(self, *args, **kwargs):
        self._axis_params.padding_mode = self.getPaddingMode()

    def _sideChanged(self, *args, **kwargs):
        self._axis_params.side = self.getSide()

    def getPaddingMode(self):
        if self._padding_widget.isChecked():
            return self._qbPaddingMode.currentText()
        else:
            return None

    def setPaddingMode(self, mode):
        index = self._qbPaddingMode.findText(mode)
        if index >= 0:
            self._qbPaddingMode.setCurrentIndex(index)

    def setAxisParams(self, axis):
        old = self.blockSignals(True)
        if self._axis_params is not None:
            self._axis_params.sigChanged.disconnect(self._axis_params_changed)
        self._axis_params = axis
        self._axis_params.sigChanged.connect(self._axis_params_changed)
        self._axis_params_changed()
        self.blockSignals(old)

    def _axis_params_changed(self, *args, **kwargs):
        self.setMode(self._axis_params.mode)
        self.setEstimatedCorValue(self._axis_params.estimated_cor)
        self.setSide(self._axis_params.side)
        self.setPaddingMode(self._axis_params.padding_mode)


class _InputWidget(qt.QWidget):
    """Widget used to define the radio to use for axis calculation from
    radios"""

    def __init__(self, parent=None, axis_params=None):
        assert isinstance(axis_params, QAxisRP)
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())

        self._angleModeWidget = _AngleModeGroupBox(parent=self, axis_params=axis_params)
        self.layout().addWidget(self._angleModeWidget)
        self._axis_params = axis_params

        self._spacer = qt.QWidget(self)
        self._spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(self._spacer)

        # expose API
        self.setScanRange = self._angleModeWidget.setScanRange

    def setAxisParams(self, axis_params):
        self._angleModeWidget.setAxisParams(axis_params)
        self._axis_params = axis_params


class _AngleModeGroupBox(qt.QGroupBox):
    """Group box to select the angle to used for cor calculation
    (0-180, 90-270 or manual)"""

    def __init__(self, parent=None, axis_params=None):
        assert isinstance(axis_params, QAxisRP)
        qt.QGroupBox.__init__(
            self, parent=parent, title="Angles to use for axis calculation"
        )
        self._corButtonsGps = qt.QButtonGroup(parent=self)
        self._corButtonsGps.setExclusive(True)
        self.setLayout(qt.QGridLayout())
        self._qrbCOR_0_180 = qt.QRadioButton("0-180", parent=self)
        self.layout().addWidget(self._qrbCOR_0_180, 0, 0)
        self._qrbCOR_90_270 = qt.QRadioButton("90-270", parent=self)
        self._qrbCOR_90_270.setToolTip(
            "pick radio closest to angles 90° and "
            "270°. If disable mean that the scan "
            "range is 180°"
        )
        self.layout().addWidget(self._qrbCOR_90_270, 0, 1)
        self._qrbCOR_manual = qt.QRadioButton("manual selection", parent=self)
        self._qrbCOR_manual.setVisible(False)
        self.layout().addWidget(self._qrbCOR_manual, 0, 2)
        # add all button to the button group
        for b in (self._qrbCOR_0_180, self._qrbCOR_90_270, self._qrbCOR_manual):
            self._corButtonsGps.addButton(b)

        self.setAxisParams(axis_params)

        # connect signal / Slot
        self._corButtonsGps.buttonClicked.connect(self._angleModeChanged)

    def setScanRange(self, scanRange):
        if scanRange == 180:
            self._qrbCOR_90_270.setEnabled(False)
            if self._qrbCOR_90_270.isChecked():
                self._qrbCOR_0_180.setChecked(True)

    def setAngleMode(self, mode):
        """ "

        :param mode: mode to use (can be manual , 90-270 or 0-180)
        """
        assert isinstance(mode, CorAngleMode)
        if mode == CorAngleMode.use_0_180:
            self._qrbCOR_0_180.setChecked(True)
        elif mode == CorAngleMode.use_90_270:
            self._qrbCOR_90_270.setChecked(True)
        else:
            self._qrbCOR_manual.setChecked(True)

    def getAngleMode(self):
        """

        :return: the angle to use for the axis calculation
        :rtype: CorAngleMode
        """
        if self._qrbCOR_90_270.isChecked():
            return CorAngleMode.use_90_270
        elif self._qrbCOR_0_180.isChecked():
            return CorAngleMode.use_0_180
        else:
            return CorAngleMode.manual_selection

    def setAxisParams(self, axis_params):
        old = self.blockSignals(True)
        self._axis_params = axis_params
        # set up
        self.setAngleMode(axis_params.angle_mode)
        self.blockSignals(old)

    def _angleModeChanged(self, *args, **kwargs):
        self._axis_params.angle_mode = self.getAngleMode()
