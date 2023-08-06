# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2017 European Synchrotron Radiation Facility
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
__date__ = "28/04/2020"


import tempfile
import unittest
import shutil
import time
import os
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt
from tomwer.test.utils import skip_gui_test
from tomwer.core.utils.scanutils import MockBlissAcquisition
from orangecontrib.tomwer.widgets.control.DataListenerOW import DataListenerOW
from tomwer.core.process.control.datalistener.rpcserver import BlissAcquisition
from tomwer.core import settings
from glob import glob


@unittest.skip("Fail on CI...")
@unittest.skipIf(skip_gui_test(), reason="skip gui test")
class TestDataListenerSynchronization(TestCaseQt):
    """Insure synchronization is working with the orangecontrib widget"""

    def setUp(self):
        super(TestDataListenerSynchronization, self).setUp()
        self._src_dir = tempfile.mkdtemp()
        self._dst_dir = tempfile.mkdtemp()
        # mock lbsram
        settings.mock_lsbram(True)
        settings._set_lbsram_path(self._src_dir)
        settings._set_dest_path(self._dst_dir)

        scan_path = os.path.join(self._src_dir, "scan0000")
        self.mock_scan = MockBlissAcquisition(
            n_sample=1,
            n_sequence=1,
            n_scan_per_sequence=3,
            n_darks=2,
            n_flats=2,
            output_dir=scan_path,
        )

        self.bliss_acquisition = BlissAcquisition(
            file_path=self.mock_scan.samples[0].sample_file,
            proposal_file=self.mock_scan.proposal_file,
            sample_file=self.mock_scan.samples[0].sample_file,
            entry_name="self.entry = '/1'",
            start_time=time.ctime(),
        )

        self.widget = DataListenerOW()

    def tearDown(self):
        self.widget.activate(False)
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        shutil.rmtree(self._src_dir)
        shutil.rmtree(self._dst_dir)
        super(TestDataListenerSynchronization, self).tearDown()

    def testSynchronization(self):
        """Make sure the datalistener will launch a synchronization on the
        data dir when receive it"""
        self.assertEqual(len(os.listdir(self._dst_dir)), 0)
        self.widget.activate(True)

        self.widget.get_listening_thread()._rpc_sequence_started(
            saving_file=self.bliss_acquisition.sample_file,
            scan_title="toto",
            sequence_scan_number="1",
            proposal_file=self.bliss_acquisition.proposal_file,
            sample_file=self.bliss_acquisition.sample_file,
        )
        time.sleep(1.0)
        self.assertEqual(self.widget._get_n_scan_observe(), 1)
        self.assertEqual(len(os.listdir(self._dst_dir)), 1)
        self.widget.get_listening_thread()._rpc_sequence_ended(
            saving_file=self.bliss_acquisition.sample_file,
            sequence_scan_number="1",
            success=True,
        )
        nx_pattern = os.path.join(self.mock_scan.samples[0].sample_directory, "*.nx")
        self.assertEqual(len(glob(nx_pattern)), 0)
        for i in range(8):
            self.qapp.processEvents()
            time.sleep(1.0)
        # check .nx file has been created
        #
        self.assertEqual(len(glob(nx_pattern)), 1)


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestDataListenerSynchronization,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
