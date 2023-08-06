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
__date__ = "11/12/2017"


import os
import shutil
import tempfile
import unittest

import fabio
import numpy
from silx.gui.utils.testutils import TestCaseQt

from tomwer.core.utils.scanutils import MockEDF
from tomwer.core.process.reconstruction.darkref.darkrefs import DarkRefs
from tomwer.core.process.reconstruction.darkref.params import DKRFRP
from tomwer.core.process.reconstruction.darkref.params import Method
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.test.utils import UtilsTest


class TestDarkRefsBehavior(TestCaseQt):
    """Test that the Darks and reference are correctly computed from the
    DarksRefs class
    """

    def setUp(self):
        TestCaseQt.setUp(self)
        self.datasetsID = ("test10",)  # TODO: add D2_H2_T2_h_ also
        self.tmpDir = tempfile.mkdtemp()
        self.foldersTest = []
        self.thRef = {}
        """number of theoretical ref file the algorithm should create"""
        self.thDark = {}
        """number of theoretical dark file the algorithm should create"""
        for dataset in self.datasetsID:
            folderTest = os.path.join(self.tmpDir, dataset)
            self.foldersTest.append(folderTest)
            dataDir = UtilsTest.getEDFDataset(dataset)
            shutil.copytree(dataDir, folderTest)
            files = os.listdir(folderTest)
            for _f in files:
                if _f.startswith(("refHST", "darkHST", "dark.edf")):
                    os.remove(os.path.join(folderTest, _f))

        self.darkRef = DarkRefs()
        self.recons_params = DKRFRP()
        self.darkRef.set_recons_params(self.recons_params)

        self.darkRef.setForceSync(True)
        # TODO: this should be define in DKRFRP() instance
        self.darkRef.DARKHST_PREFIX = "darkHST"
        self.recons_params._set_remove_opt(False)

    def tearDown(self):
        self.qapp.processEvents()
        self.darkRef = None
        shutil.rmtree(self.tmpDir)
        TestCaseQt.tearDown(self)

    def testDarkCreation(self):
        """Test that the dark is correctly computed"""
        self.recons_params.ref_calc_method = Method.none
        self.recons_params.dark_calc_method = Method.median

        for folderTest in self.foldersTest:
            datasetName = os.path.basename(folderTest)
            with self.subTest(dataset=datasetName):
                self.darkRef.process(folderTest)
                self.qapp.processEvents()
                if os.path.basename(folderTest) == "test10":
                    self.assertTrue("darkend0000.edf" in os.listdir(folderTest))
                    self.assertTrue("dark.edf" in os.listdir(folderTest))
                    self.assertTrue(
                        len(
                            self.darkRef.getDarkHSTFiles(
                                folderTest, prefix=self.recons_params.dark_prefix
                            )
                        )
                        is 1
                    )
                    self.assertTrue(
                        len(
                            self.darkRef.getRefHSTFiles(
                                folderTest, prefix=self.recons_params.ref_prefix
                            )
                        )
                        is 0
                    )
                elif os.path.basename(folderTest) == "D2_H2_T2_h_":
                    self.assertTrue("darkend0000.edf" in os.listdir(folderTest))
                    # check ref are not deleted
                    for ref in (
                        "ref0000_3600.edf",
                        "ref0028_3600.edf",
                        "ref0044_0000.edf",
                    ):
                        self.assertTrue(ref in os.listdir(folderTest))
                    self.assertTrue("dark0000.edf" in os.listdir(folderTest))
                    self.assertFalse("refHST0000.edf" in os.listdir(folderTest))
                    self.assertFalse("refHST3600.edf" in os.listdir(folderTest))

    def testRefCreation(self):
        """Test that the dark is correctly computed"""
        self.recons_params.ref_calc_method = Method.median
        self.recons_params.dark_calc_method = Method.none

        for folderTest in self.foldersTest:
            datasetName = os.path.basename(folderTest)
            with self.subTest(dataset=datasetName):
                self.darkRef.process(folderTest)
                self.qapp.processEvents()
                if os.path.basename(folderTest) == "test10":
                    self.assertTrue("darkend0000.edf" in os.listdir(folderTest))
                    self.assertFalse("dark0000.edf" in os.listdir(folderTest))
                    self.assertTrue("refHST0000.edf" in os.listdir(folderTest))
                    self.assertTrue("refHST0020.edf" in os.listdir(folderTest))
                    self.assertTrue("ref0000_0000.edf" in os.listdir(folderTest))
                    self.assertTrue("ref0000_0020.edf" in os.listdir(folderTest))
                    self.assertTrue("ref0001_0000.edf" in os.listdir(folderTest))
                    self.assertTrue("ref0001_0020.edf" in os.listdir(folderTest))
                elif os.path.basename(folderTest) == "D2_H2_T2_h_":
                    # check ref are not deleted
                    for ref in (
                        "ref0000_3600.edf",
                        "ref0028_3600.edf",
                        "ref0044_0000.edf",
                    ):
                        self.assertTrue(ref in os.listdir(folderTest))
                    self.assertTrue("darkend0000.edf" in os.listdir(folderTest))
                    self.assertTrue("refHST0000.edf" in os.listdir(folderTest))
                    self.assertTrue("refHST3600.edf" in os.listdir(folderTest))

    def testRemoveOption(self):
        """Test that the remove option is working"""
        self.recons_params.ref_calc_method = Method.none
        self.recons_params.dark_calc_method = Method.none
        self.recons_params._set_remove_opt(True)
        for folderTest in self.foldersTest:
            datasetName = os.path.basename(folderTest)
            with self.subTest(dataset=datasetName):
                self.darkRef.process(folderTest)
                self.qapp.processEvents()
                if os.path.basename(folderTest) == "test10":
                    self.assertFalse("darkend0000.edf" in os.listdir(folderTest))
                    self.assertFalse("dark0000.edf" in os.listdir(folderTest))
                    self.assertFalse("refHST0000.edf" in os.listdir(folderTest))
                    self.assertFalse("refHST0020.edf" in os.listdir(folderTest))
                    self.assertFalse("ref0000_0000.edf" in os.listdir(folderTest))
                    self.assertFalse("ref0000_0020.edf" in os.listdir(folderTest))
                    self.assertFalse("ref0001_0000.edf" in os.listdir(folderTest))
                    self.assertFalse("ref0001_0020.edf" in os.listdir(folderTest))
                elif os.path.basename(folderTest) == "D2_H2_T2_h_":
                    # check ref are not deleted
                    for ref in (
                        "ref0000_3600.edf",
                        "ref0028_3600.edf",
                        "ref0044_0000.edf",
                    ):
                        self.assertFalse(ref in os.listdir(folderTest))
                    self.assertFalse("darkend0000.edf" in os.listdir(folderTest))
                    self.assertFalse("refHST0000.edf" in os.listdir(folderTest))
                    self.assertFalse("refHST3600.edf" in os.listdir(folderTest))
                    self.assertFalse("dark0000.edf" in os.listdir(folderTest))

    def testSkipOption(self):
        """Test that the overwrite option is working"""
        self.recons_params.ref_calc_method = Method.none
        self.recons_params.dark_calc_method = Method.none
        self.recons_params._set_skip_if_exist(True)

        for folderTest in self.foldersTest:
            datasetName = os.path.basename(folderTest)
            with self.subTest(dataset=datasetName):
                iniRefNFile = len(
                    self.darkRef.getRefHSTFiles(
                        folderTest, prefix=self.recons_params.ref_prefix
                    )
                )
                iniDarkNFile = len(
                    self.darkRef.getDarkHSTFiles(
                        folderTest, prefix=self.recons_params.dark_prefix
                    )
                )
                self.darkRef.process(folderTest)
                self.qapp.processEvents()
                refs = self.darkRef.getRefHSTFiles(
                    folderTest, prefix=self.recons_params.ref_prefix
                )
                darks = self.darkRef.getDarkHSTFiles(
                    folderTest, prefix=self.recons_params.dark_prefix
                )
                self.assertTrue(len(refs) == iniRefNFile)
                self.assertTrue(len(darks) == iniDarkNFile)


class TestRefCalculationOneSerie(TestCaseQt):
    """
    Make sure the calculation is correct for the dark and flat field
    according to the method used.
    """

    def setUp(self):
        super().setUp()
        self.tmpDir = tempfile.mkdtemp()
        n_scans = 5
        n_info = 1
        n_xml = 1
        MockEDF.fastMockAcquisition(self.tmpDir, n_radio=n_scans)
        reFiles = {}
        data1 = numpy.zeros((20, 10))
        data2 = numpy.zeros((20, 10)) + 100
        reFiles["ref0000_0000.edf"] = data1
        reFiles["ref0001_0000.edf"] = data2
        reFiles["ref0002_0000.edf"] = data2
        reFiles["ref0003_0000.edf"] = data2
        for refFile in reFiles:
            file_desc = fabio.edfimage.EdfImage(data=reFiles[refFile])
            file_desc.write(os.path.join(self.tmpDir, refFile))
        assert len(os.listdir(self.tmpDir)) is (len(reFiles) + n_scans + n_xml + n_info)

        self.recons_params = DKRFRP()
        self.darkRef = DarkRefs(reconsparams=self.recons_params)
        self.darkRef.setForceSync(True)
        self.recons_params.ref_pattern = "ref*.*[0-9]{3,4}_[0-9]{3,4}"

    def tearDown(self):
        shutil.rmtree(self.tmpDir)
        super().tearDown()

    def testRefMedianCalculation(self):
        self.recons_params.ref_calc_method = Method.median
        self.recons_params.dark_calc_method = Method.none
        self.darkRef.process(self.tmpDir)
        refHST = os.path.join(self.tmpDir, "refHST0000.edf")
        self.assertTrue(os.path.isfile(refHST))

        self.assertTrue(
            numpy.array_equal(fabio.open(refHST).data, numpy.zeros((20, 10)) + 100)
        )

    def testRefMeanCalculation(self):
        self.recons_params.ref_calc_method = Method.average
        self.recons_params.dark_calc_method = Method.none
        self.darkRef.process(self.tmpDir)
        refHST = os.path.join(self.tmpDir, "refHST0000.edf")
        self.assertTrue(os.path.isfile(refHST))
        self.assertTrue(
            numpy.array_equal(fabio.open(refHST).data, numpy.zeros((20, 10)) + 75)
        )


class TestRefCalculationThreeSerie(TestCaseQt):
    """
    Make sure the calculation is correct for the dark and flat field
    according to the method used.
    """

    def setUp(self):
        super().setUp()
        self.tmpDir = tempfile.mkdtemp()
        MockEDF.fastMockAcquisition(folder=self.tmpDir, n_radio=1)
        reFiles = {}
        self.series = (0, 10, 200)
        for serie in self.series:
            data1 = numpy.zeros((20, 10)) + serie
            data2 = numpy.zeros((20, 10)) + 100 + serie
            reFiles["ref0000_" + str(serie).zfill(4) + ".edf"] = data1
            reFiles["ref0001_" + str(serie).zfill(4) + ".edf"] = data2
            reFiles["ref0002_" + str(serie).zfill(4) + ".edf"] = data2
            reFiles["ref0003_" + str(serie).zfill(4) + ".edf"] = data2
            for refFile in reFiles:
                file_desc = fabio.edfimage.EdfImage(data=reFiles[refFile])
                file_desc.write(os.path.join(self.tmpDir, refFile))

        self.recons_params = DKRFRP()
        self.darkRef = DarkRefs(reconsparams=self.recons_params)
        self.darkRef.setForceSync(True)
        self.recons_params.ref_pattern = "ref*.*[0-9]{3,4}_[0-9]{3,4}"

    def tearDown(self):
        shutil.rmtree(self.tmpDir)
        super().tearDown()

    def testRefMedianCalculation(self):
        self.recons_params.ref_calc_method = Method.median
        self.recons_params.dark_calc_method = Method.none
        self.darkRef.process(self.tmpDir)
        for serie in self.series:
            refHST = os.path.join(self.tmpDir, "refHST" + str(serie).zfill(4) + ".edf")
            self.assertTrue(os.path.isfile(refHST))
            self.assertTrue(
                numpy.array_equal(
                    fabio.open(refHST).data, numpy.zeros((20, 10)) + 100 + serie
                )
            )

    def testRefMeanCalculation(self):
        self.recons_params.ref_calc_method = Method.average
        self.recons_params.dark_calc_method = Method.none
        self.darkRef.process(self.tmpDir)
        for serie in self.series:
            refHST = os.path.join(self.tmpDir, "refHST" + str(serie).zfill(4) + ".edf")
            self.assertTrue(os.path.isfile(refHST))
            self.assertTrue(
                numpy.array_equal(
                    fabio.open(refHST).data, numpy.zeros((20, 10)) + 75 + serie
                )
            )


class TestDarkCalculationOneFrame(TestCaseQt):
    """Make sure computation of the Dark is correct"""

    def setUp(self):
        super().setUp()
        self.tmpDir = tempfile.mkdtemp()
        n_scan = 1
        n_info = 1
        n_xml = 1
        MockEDF.fastMockAcquisition(self.tmpDir, n_radio=n_scan)
        file_desc = fabio.edfimage.EdfImage(data=numpy.zeros((20, 10)) + 10)

        file_desc.write(os.path.join(self.tmpDir, "darkend0000.edf"))
        assert len(os.listdir(self.tmpDir)) is (1 + n_scan + n_info + n_xml)
        self.recons_params = DKRFRP()
        self.darkRef = DarkRefs(reconsparams=self.recons_params)
        self.darkRef.setForceSync(True)

    def tearDown(self):
        shutil.rmtree(self.tmpDir)
        super().tearDown()

    def testDarkMeanCalculation(self):
        self.recons_params.ref_calc_method = Method.none
        self.recons_params.dark_calc_method = Method.average

        self.darkRef.process(self.tmpDir)
        refHST = os.path.join(self.tmpDir, "dark.edf")
        self.assertTrue(os.path.isfile(refHST))
        self.assertTrue(
            numpy.array_equal(fabio.open(refHST).data, numpy.zeros((20, 10)) + 10)
        )

    def testDarkMedianCalculation(self):
        self.recons_params.ref_calc_method = Method.none
        self.recons_params.dark_calc_method = Method.median

        self.darkRef.process(self.tmpDir)
        refHST = os.path.join(self.tmpDir, "dark.edf")
        self.assertTrue(os.path.isfile(refHST))

        self.assertTrue(
            numpy.array_equal(fabio.open(refHST).data, numpy.zeros((20, 10)) + 10)
        )


class TestDarkCalculation(TestCaseQt):
    """Make sure computation of the Dark is correct"""

    def setUp(self):
        super().setUp()
        self.tmpDir = tempfile.mkdtemp()
        n_scan = 1
        n_xml = 1
        n_info = 1
        MockEDF.fastMockAcquisition(os.path.join(self.tmpDir), n_radio=n_scan)

        file_desc = fabio.edfimage.EdfImage(data=numpy.zeros((20, 10)))
        file_desc.append_frame(data=(numpy.zeros((20, 10)) + 100))
        file_desc.append_frame(data=(numpy.zeros((20, 10)) + 100))
        file_desc.append_frame(data=(numpy.zeros((20, 10)) + 100))

        file_desc.write(os.path.join(self.tmpDir, "darkend0000.edf"))
        assert len(os.listdir(self.tmpDir)) is (1 + n_scan + n_xml + n_info)
        self.darkRef = DarkRefs()
        self.recons_params = DKRFRP()
        self.darkRef.set_recons_params(self.recons_params)
        self.darkRef.setForceSync(True)

    def tearDown(self):
        shutil.rmtree(self.tmpDir)
        super().tearDown()

    def testDarkMeanCalculation(self):
        self.recons_params.ref_calc_method = Method.none
        self.recons_params.dark_calc_method = Method.average

        self.darkRef.process(self.tmpDir)
        refHST = os.path.join(self.tmpDir, "dark.edf")
        self.assertTrue(os.path.isfile(refHST))
        self.assertTrue(
            numpy.array_equal(fabio.open(refHST).data, numpy.zeros((20, 10)) + 75)
        )

    def testDarkMedianCalculation(self):
        self.recons_params.ref_calc_method = Method.none
        self.recons_params.dark_calc_method = Method.median

        self.darkRef.process(self.tmpDir)
        refHST = os.path.join(self.tmpDir, "dark.edf")
        self.assertTrue(os.path.isfile(refHST))

        self.assertTrue(
            numpy.array_equal(fabio.open(refHST).data, numpy.zeros((20, 10)) + 100)
        )


class TestDarkAccumulation(TestCaseQt):
    """
    Make sure computation for dark in accumulation are correct
    """

    def setUp(self):
        super().setUp()
        self.dataset = "bone8_1_"
        dataDir = UtilsTest.getEDFDataset(self.dataset)
        self.outputdir = tempfile.mkdtemp()
        shutil.copytree(src=dataDir, dst=os.path.join(self.outputdir, self.dataset))
        self.darkFile = os.path.join(self.outputdir, self.dataset, "dark.edf")
        # create a single 'bone8_1_' to be a valid acquisition directory
        MockEDF.fastMockAcquisition(os.path.join(self.outputdir, self.dataset))
        assert os.path.isfile(self.darkFile)
        with fabio.open(self.darkFile) as dsc:
            self.dark_reference = dsc.data
        # remove dark file
        os.remove(self.darkFile)

        self.recons_params = DKRFRP()
        self.darkRef = DarkRefs()
        self.darkRef.setForceSync(True)
        self.recons_params.ref_calc_method = Method.none
        self.recons_params.dark_calc_method = Method.median
        self.recons_params.dark_pattern = "darkend*"
        # TODO: the prefix should also be embeded in the DKRFRP
        self.recons_params.dark_prefix = "dark.edf"

    def tearDown(self):
        shutil.rmtree(self.outputdir)
        super().tearDown()

    def testComputation(self):
        """Test data bone8_1_ from id16b containing dark.edf of reference
        and darkend"""
        self.darkRef.process(os.path.join(self.outputdir, self.dataset))
        self.assertTrue(os.path.isfile(self.darkFile))
        with fabio.open(self.darkFile) as dsc:
            self.computed_dark = dsc.data
        self.assertTrue(numpy.array_equal(self.computed_dark, self.dark_reference))


class TestPCOTomo(TestCaseQt):
    """Test processing of DKRF are correct"""

    def setUp(self):
        TestCaseQt.setUp(self)
        self.tmpDir = tempfile.mkdtemp()
        MockEDF.fastMockAcquisition(self.tmpDir)

        self.darkRef = DarkRefs()
        self.recons_params = DKRFRP()
        self.darkRef.set_recons_params(self.recons_params)
        self.darkRef.setForceSync(True)
        self.recons_params.ref_calc_method = Method.none
        self.recons_params.dark_calc_method = Method.none
        self.recons_params.dark_pattern = ".*_dark_.*"
        self.recons_params.ref_pattern = ".*_ref_.*"
        self.recons_params._set_remove_opt(True)
        # TODO: the prefix should also be embeded in the DKRFRP
        self.darkRef.DARKHST_PREFIX = "darkHST"

    def copyDataset(self, dataset):
        folder = os.path.join(self.tmpDir, dataset)
        shutil.copytree(os.path.join(UtilsTest.getEDFDataset(dataset)), folder)
        self.scan = ScanFactory.create_scan_object(scan_path=folder)

    def tearDown(self):
        shutil.rmtree(self.tmpDir)
        TestCaseQt.tearDown(self)

    def testDark3Scan(self):
        """
        Make sure the processing dark field for
        pcotomo_3scan_refdarkbeg_end_download are correct
        """
        self.dataset = "pcotomo_3scan_refdarkbeg_end_download"
        self.copyDataset(self.dataset)
        _file = os.path.join(
            self.tmpDir, "pcotomo_3scan_refdarkbeg_end_download", "dark.edf"
        )
        if os.path.isfile(_file):
            os.remove(_file)
        self.recons_params.dark_calc_method = Method.median
        self.darkRef.process(self.scan)
        darkHSTFiles = self.darkRef.getDarkHSTFiles(
            self.scan.path, prefix=self.recons_params.dark_prefix
        )
        self.assertTrue(len(darkHSTFiles) is 2)
        dark0000 = os.path.join(self.scan.path, "dark0000.edf")
        dark1000 = os.path.join(self.scan.path, "dark1000.edf")
        self.assertTrue(dark0000 in darkHSTFiles)
        self.assertTrue(dark1000 in darkHSTFiles)

    def testRef3Scan(self):
        """
        Make sure the processing flat field for
        pcotomo_3scan_refdarkbeg_end_download are correct
        """
        self.dataset = "pcotomo_3scan_refdarkbeg_end_download"
        self.copyDataset(self.dataset)
        self.recons_params.ref_calc_method = Method.median
        self.darkRef.process(self.scan)
        refHSTFiles = self.darkRef.getRefHSTFiles(
            self.scan.path, prefix=self.recons_params.ref_prefix
        )
        self.assertTrue(len(refHSTFiles) is 2)
        f0000 = os.path.join(self.scan.path, "refHST0000.edf")
        self.assertTrue(f0000 in refHSTFiles)
        f1000 = os.path.join(self.scan.path, "refHST1000.edf")
        self.assertTrue(f1000 in refHSTFiles)

    def testDark2x2Scan(self):
        self.dataset = "pcotomo_2x2scan_refdarkbeg_end_conti"
        self.copyDataset(self.dataset)
        self.recons_params.dark_calc_method = Method.median
        self.darkRef.process(self.scan)

    def testRef2x2Scan(self):
        self.dataset = "pcotomo_2x2scan_refdarkbeg_end_conti"
        self.copyDataset(self.dataset)
        self.recons_params.ref_calc_method = Method.median
        self.darkRef.process(self.scan)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (
        TestDarkRefsBehavior,
        TestRefCalculationOneSerie,
        TestRefCalculationThreeSerie,
        TestDarkCalculationOneFrame,
        TestDarkCalculation,
        TestPCOTomo,
        TestDarkAccumulation,
    ):

        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
