# coding: utf-8
###########################################################################
# Copyright (C) 2016-2019 European Synchrotron Radiation Facility
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
#############################################################################

__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "28/08/2020"


from silx.gui import qt
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.settings import get_lbsram_path, isOnLbsram
from tomwer.core.utils import isLowOnMemory
from ..processingstack import FIFO, ProcessingThread
from tomwer.core.process.edit import darkflatpatch
from silx.io.url import DataUrl
import logging

_logger = logging.getLogger(__name__)


class DarkFlatPatchProcessStack(FIFO, qt.QObject):
    """Implementation of the `.AxisProcess` but having a stack for treating
    scans and making computation in threads"""

    def __init__(self, parent=None):
        qt.QObject.__init__(self, parent=parent)
        FIFO.__init__(self)
        self._dry_run = False

    def _process(self, scan, configuration, callback=None):
        _logger.info("dark-flat patch stack is processing {}".format(str(scan)))
        self._scan_currently_computed = scan
        assert isinstance(scan, TomwerScanBase)
        self._computationThread.finished.connect(self._end_threaded_computation)

        if isOnLbsram(scan) and isLowOnMemory(get_lbsram_path()) is True:
            # if computer is running into low memory on lbsram skip it
            mess = "low memory, skip dark-flat-patch reconstruction for", scan.path
            _logger.processSkipped(mess)
            self._end_threaded_computation()
        else:
            self._computationThread.init(scan=scan, configuration=configuration)
            # need to manage connect before starting it because
            self._computationThread.start()

    def _end_threaded_computation(self, callback=None):
        self._computationThread.finished.disconnect(self._end_threaded_computation)
        super()._end_threaded_computation(callback=callback)

    def _create_processing_thread(self) -> qt.QThread:
        return _DarkFlatPatchProcessingThread()


class _DarkFlatPatchProcessingThread(ProcessingThread):
    """
    Thread use to execute the processing of dark-flat patch
    """

    def __init__(self):
        ProcessingThread.__init__(self)
        self._scan = None
        self._configuration = None

    def init(self, scan, configuration):
        self._scan = scan
        self._configuration = configuration

    def run(self):
        self.sigComputationStarted.emit()
        _logger.processStarted("Start dark-flat patch".format(str(self._scan)))
        try:
            darkflatpatch.apply_dark_flat_patch(
                config=self._configuration, scan=self._scan
            )
        except Exception as e:
            _logger.processFailed(
                "Fail to patch dark-flat for {}. Reason is "
                "{}".format(str(self._scan), e)
            )
        else:
            index = self._scan.pop_process_index()
            if isinstance(self._scan, EDFTomoScan):
                entry = None
            else:
                entry = self._scan.entry
            configuration_to_dump = self._configuration
            keys = list(configuration_to_dump.keys())
            for key in keys:
                if isinstance(configuration_to_dump[key], DataUrl):
                    configuration_to_dump[key] = configuration_to_dump[key].path()

            darkflatpatch.DarkFlatPatch._register_process(
                process_file=self._scan.process_file,
                entry=entry,
                configuration=configuration_to_dump,
                results={},
                process=darkflatpatch.DarkFlatPatch,
                process_index=index,
                overwrite=True,
            )
            _logger.processSucceed(
                "Dark-flat patched for {}." "".format(str(self._scan))
            )
