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
__date__ = "28/10/2020"


from Orange.widgets.widget import Input, Output
from Orange.widgets import widget, gui
from tomwer.web.client import OWClient
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.gui.edit.imagekeyeditor import ImageKeyDialog
from tomwer.synctools.stacks.edit.imagekeyeditor import ImageKeyEditorProcessStack
from ..utils import WidgetLongProcessing
import logging

_logger = logging.getLogger(__name__)


class ImageKeyEditorOW(widget.OWWidget, OWClient, WidgetLongProcessing):
    """
    Widget to define on the fly the image_key of a HDF5TomoScan
    """

    name = "image-key-editor"
    id = "orange.widgets.tomwer.control.ImageKeyEditorOW.ImageKeyEditorOW"
    description = "Interface to edit `image_key` of nexus files"
    icon = "icons/image_key_editor.svg"
    priority = 24
    category = "esrfWidgets"
    keywords = ["hdf5", "nexus", "tomwer", "file", "edition", "NXTomo", "editor"]

    want_main_area = True
    resizing_enabled = True
    compress_signal = False

    class Inputs:
        data_in = Input(name="data", type=TomwerScanBase)

    class Outputs:
        data_out = Output(name="data", type=TomwerScanBase)

    def __init__(self, parent=None):
        widget.OWWidget.__init__(self, parent)
        OWClient.__init__(self)
        WidgetLongProcessing.__init__(self)
        self._scan = None
        self._processingStack = ImageKeyEditorProcessStack(self)
        layout = gui.vBox(self.mainArea, self.name).layout()

        self.widget = ImageKeyDialog(parent=self)
        layout.addWidget(self.widget)

        # connect signal / slot
        self.widget.sigValidated.connect(self._validateCallback)
        self._processingStack.sigComputationStarted.connect(self._startProcessing)
        self._processingStack.sigComputationEnded.connect(self._endProcessing)

    @Inputs.data_in
    def process(self, scan):
        if scan is None:
            return
        elif not isinstance(scan, HDF5TomoScan):
            _logger.error("You can only edit image keys for the HDF5 scans")
        else:
            self._scan = scan
            self.widget.setScan(scan)
            self.activateWindow()
            self.raise_()
            self.show()

    def getConfiguration(self):
        return {
            "modifications": self.widget.getModifications(),
        }

    def _validateCallback(self):
        if self._scan is None:
            return
        self._processingStack.add(self._scan, configuration=self.getConfiguration())

    def _endProcessing(self, scan):
        WidgetLongProcessing._endProcessing(self, scan)
        if scan is not None:
            self.Outputs.data_out.send(scan)
