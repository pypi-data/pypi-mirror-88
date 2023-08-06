# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2017-2019 European Synchrotron Radiation Facility
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
__date__ = "27/02/2019"


from tomwer.gui.reconstruction.axis import AxisWindow
from tomwer.test.utils import skip_gui_test
from tomwer.test.utils import UtilsTest
from tomwer.core.process.reconstruction.axis.mode import AxisMode
from tomwer.core.process.reconstruction.axis.params import AxisCalculationInput
from tomwer.core.process.reconstruction.axis.projectiontype import ProjectionType
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.synctools.axis import QAxisRP
from silx.gui.utils.testutils import TestCaseQt
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomoscan.scanbase import _FOV
from silx.gui import qt
import numpy.random
import unittest
import tempfile
import os
import shutil
import h5py


@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestWindowAxis(TestCaseQt):
    """Test that the axis widget work correctly"""

    def setUp(self):
        self.recons_params = QAxisRP()
        self._window = AxisWindow(axis_params=self.recons_params)
        self.scan_path = UtilsTest.getEDFDataset("D2_H2_T2_h_")
        self.scan = EDFTomoScan(self.scan_path)
        self._window.show()
        self.qWaitForWindowExposed(self._window)

    def tearDown(self):
        self._window.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._window.close()

    def testSetImagesNumpyArray(self):
        """Test the setImages function"""
        radio_axis = self._window._axisWidget._radioAxis
        self.assertEqual(radio_axis.getPlot().getPlot().getActiveImage(), None)
        imgA = numpy.random.random((100, 100))
        imgB = numpy.random.random((100, 100))
        radio_axis.setImages(imgA=imgA, imgB=imgB)
        self.qapp.processEvents()
        self.assertNotEqual(radio_axis.getPlot().getPlot().getActiveImage(), None)

    def testSetScan(self):
        """Test the setScan function"""
        radio_axis_plot = self._window._axisWidget._radioAxis.getPlot()
        self.assertEqual(radio_axis_plot.getPlot().getActiveImage(), None)
        self._window.setScan(self.scan)
        self.assertNotEqual(radio_axis_plot.getPlot().getActiveImage(), None)

    def testShiftButtons(self):
        """Test that the 'left', 'right', ... buttons and the shift steps are
        correctly working"""
        imgA = numpy.random.random((100, 100))
        imgB = numpy.random.random((100, 100))
        radio_axis = self._window._axisWidget._radioAxis
        radio_axis.setImages(imgA=imgA, imgB=imgB)
        self.qapp.processEvents()
        self.assertTrue(radio_axis.getXShift() == 0)
        self.assertTrue(radio_axis.getYShift() == 0)
        self.assertTrue(radio_axis.getShiftStep() == 1.0)
        radio_axis._controlWidget._shiftControl._leftButton.click()
        self.qapp.processEvents()
        self.assertTrue(radio_axis.getXShift() == -1)
        self.assertTrue(radio_axis.getYShift() == 0)
        radio_axis._controlWidget._shiftControl._rightButton.click()
        self.qapp.processEvents()
        self.assertTrue(radio_axis.getXShift() == 0)
        self.assertTrue(radio_axis.getYShift() == 0)
        radio_axis._controlWidget._displacementSelector._fineButton.toggle()
        self.qapp.processEvents()
        self.assertTrue(radio_axis.getShiftStep() == 0.1)
        radio_axis._controlWidget._shiftControl._topButton.click()
        self.qapp.processEvents()
        self.assertTrue(radio_axis.getXShift() == 0)
        self.assertTrue(radio_axis.getYShift() == 0.1)
        radio_axis.setShiftStep(0.2)
        self.assertTrue(radio_axis.getShiftStep() == 0.2)
        radio_axis._controlWidget._shiftControl._bottomButton.click()
        self.qapp.processEvents()
        self.assertTrue(radio_axis.getXShift() == 0)
        self.assertTrue(radio_axis.getYShift() == -0.1)

    def testAxisObjectGlobal(self):
        """Test that the GUI change according to the Axis object"""
        axis_obj = QAxisRP()
        self._window.setReconsParams(axis_obj)
        self.qapp.processEvents()
        self.assertEqual(
            self._window._axisWidget._radioAxis.getMode(), AxisMode.centered
        )
        # TODO: change the mode to see if the object is modify

    def testAxisObjectManual(self):
        """Test that the GUI change according to the Axis object"""
        axis_params = QAxisRP()
        axis_params.mode = AxisMode.manual
        axis_params.set_value_ref_tomwer(-6.0)
        # note : for now only the xshift is managed !
        self._window.setReconsParams(axis_params)
        radio_axis = self._window._axisWidget._radioAxis
        self.assertEqual(radio_axis.getMode(), AxisMode.manual)
        self.assertEqual(radio_axis.getXShift(), -6.0)
        self.assertEqual(radio_axis.getYShift(), 0.0)

    def testAxisCalculationUpdate(self):
        """Test that the ReconsParam object and the gui are synchronized"""
        self.recons_params = QAxisRP()
        self._window = AxisWindow(axis_params=self.recons_params)
        main_opt_widget = self._window._axisWidget._radioAxis._controlWidget._mainWidget
        self.assertTrue(
            self.recons_params.projection_type is ProjectionType.transmission
        )
        self.assertTrue(self.recons_params.paganin_preproc is False)
        self.assertTrue(
            main_opt_widget._optionsWidget._qcbDataMode.currentData(qt.Qt.UserRole)
            is AxisCalculationInput.transmission
        )
        with self.assertRaises(AttributeError):
            self.recons_params.axis.paganin_preproc = False
        with self.assertRaises(AttributeError):
            self.recons_params.axis.projection_type = ProjectionType.transmission

        # test that interface will synchronize with reconsparams
        self.recons_params.calculation_input_type = AxisCalculationInput.emission
        self.qapp.processEvents()
        self.assertTrue(
            main_opt_widget._optionsWidget._qcbDataMode.currentData(qt.Qt.UserRole)
            is AxisCalculationInput.emission
        )
        # test that reconsparams will synchronize with interface
        cal_type = AxisCalculationInput.transmission_pag.name()
        index = main_opt_widget._optionsWidget._qcbDataMode.findText(cal_type)
        assert index >= 0
        main_opt_widget._optionsWidget._qcbDataMode.setCurrentIndex(index)
        self.assertTrue(
            self.recons_params.calculation_input_type
            is AxisCalculationInput.transmission_pag
        )

    def testAxisCalculationSaveLoad(self):
        pass


@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestWindowsAxisSetScan(TestCaseQt):
    """Test that updates are correctly done in the case scan has some
    knowledge on"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self.recons_params = QAxisRP()
        self.widget = AxisWindow(axis_params=self.recons_params)
        self.scan_dir = tempfile.mkdtemp()
        # create dataset
        self.master_file = os.path.join(self.scan_dir, "frm_edftomomill_twoentries.nx")
        shutil.copyfile(
            UtilsTest.getH5Dataset(folderID="frm_edftomomill_twoentries.nx"),
            self.master_file,
        )
        self.scan = HDF5TomoScan(scan=self.master_file, entry="entry0000")

    def tearDown(self):
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        TestCaseQt.tearDown(self)

    def patch_fov(self, value: str):
        with h5py.File(self.scan.master_file, mode="a") as h5s:
            for entry in ("entry0000", "entry0001"):
                entry_node = h5s[entry]
                if "instrument/detector/field_of_view" in entry_node:
                    del entry_node["instrument/detector/field_of_view"]
                entry_node["instrument/detector/field_of_view"] = value

    def testAlgorithmUpdate(self):
        """Make sure the algorithm is updated according to the field of view"""
        self.assertEqual(self.widget.getSelection(), "radio")
        self.assertEqual(self.widget.getRadioMode(), AxisMode.centered)
        self.patch_fov(value=_FOV.HALF.value)
        self.widget.setScan(self.scan)
        self.assertEqual(self.widget.getRadioMode(), AxisMode.global_)
        self.patch_fov(value=_FOV.FULL.value)
        self.scan.clear_caches()
        self.widget.setScan(self.scan)
        self.assertEqual(self.widget.getRadioMode(), AxisMode.global_)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestWindowAxis, TestWindowsAxisSetScan):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
