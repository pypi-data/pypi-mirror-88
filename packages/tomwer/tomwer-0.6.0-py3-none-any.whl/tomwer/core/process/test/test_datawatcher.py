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
__date__ = "05/04/2019"


import shutil
import tempfile
import unittest
import os
import time

from tomwer.core.utils.scanutils import MockEDF
from tomwer.core.process.control.datawatcher import DataWatcher


class TestDataWatcherIO(unittest.TestCase):
    """Test inputs and outputs types of the handler functions"""

    def setUp(self):
        self.scan_folder = tempfile.mkdtemp()

        self.data_watcher_process = DataWatcher()
        self.data_watcher_process.setFolderObserved(self.scan_folder)
        self.data_watcher_process.setWaitTimeBtwLoop(1)
        self.scan = MockEDF.mockScan(
            scanID=self.scan_folder, nRadio=10, nRecons=1, nPagRecons=4, dim=10
        )

    def tearDown(self):
        self.data_watcher_process.stop()
        shutil.rmtree(self.scan_folder)

    # @timeout_decorator.timeout(5)
    # def testOutputTomoBase(self):
    # TODO: look why this is not working ???
    #     self.data_watcher_process.clear_output_values()
    #     self.data_watcher_process.start()
    #     self.data_watcher_process._set_return_dict(False)
    #
    #     while self.data_watcher_process.get_output_value('data') is None:
    #         time.sleep(0.5)
    #
    #     out = self.data_watcher_process.get_output_value('data')
    #     print(type(out))
    #     self.assertTrue(isinstance(out, TomoBase))

    @unittest.skipIf(os.name != "posix", reason="not tested under windows yet")
    def testOutputDict(self):
        self.data_watcher_process.clear_output_values()
        self.data_watcher_process._set_return_dict(True)
        self.data_watcher_process.start()

        timeout = 8
        while (
            self.data_watcher_process.get_output_value("data") is None and timeout > 0
        ):
            _delta = 0.5
            time.sleep(_delta)
            timeout -= _delta

        if timeout <= 0:
            self.fail("timeout expire")
        out = self.data_watcher_process.get_output_value("data")
        self.assertTrue(isinstance(out, dict))


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestDataWatcherIO,):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite
