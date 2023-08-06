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

__authors__ = ["C. Nemoz", "H. Payno"]
__license__ = "MIT"
__date__ = "25/05/2018"

from Orange.widgets import widget, gui
from Orange.widgets.widget import Output, Input
from tomwer.web.client import OWClient
from tomwer.gui.scanselectorwidget import ScanSelectorWidget
from tomwer.core.scan.scanbase import TomwerScanBase
import logging

logger = logging.getLogger(__name__)


class DataSelectorOW(widget.OWWidget, OWClient):
    name = "data selector"
    id = "orange.widgets.tomwer.scanselector"
    description = (
        "List all received scan. Then user can select a specific"
        "scan to be passed to the next widget."
    )
    icon = "icons/scanselector.svg"
    priority = 42
    category = "esrfWidgets"
    keywords = ["tomography", "selection", "tomwer", "folder"]

    want_main_area = True
    resizing_enabled = True
    compress_signal = False

    class Inputs:
        data_in = Input(name="data", type=TomwerScanBase)

    class Outputs:
        data_out = Output(name="data", type=TomwerScanBase)

    def __init__(self, parent=None):
        """"""
        widget.OWWidget.__init__(self, parent)
        OWClient.__init__(self)

        self.widget = ScanSelectorWidget(parent=self)
        self.widget.sigSelectionChanged.connect(self.changeSelection)
        layout = gui.vBox(self.mainArea, self.name).layout()
        layout.addWidget(self.widget)
        # expose API
        self.setActiveScan = self.widget.setActiveScan
        self.selectAll = self.widget.selectAll
        self.n_scan = self.widget.n_scan
        self.add = self.widget.add

    @Inputs.data_in
    def addScan(self, scan):
        if scan is not None:
            self.widget.add(scan)

    def changeSelection(self, list_scan):
        if list_scan:
            for scan_id in list_scan:
                if scan_id in self.widget.dataList._scanIDs:
                    scan = self.widget.dataList._scanIDs[scan_id]
                    assert isinstance(scan, TomwerScanBase)
                    self.Outputs.data_out.send(scan)
                else:
                    logger.error("%s not found in scan ids" % scan_id)

    def send(self):
        """send output signals for each selected items"""
        sItem = self.widget.dataList.selectedItems()
        if sItem and len(sItem) >= 1:
            selection = [_item.text() for _item in sItem]
            self.changeSelection(list_scan=selection)


if __name__ == "__main__":
    from silx.gui import qt

    qapp = qt.QApplication([])
    widget = DataSelectorOW(parent=None)
    widget.show()
    qapp.exec_()
