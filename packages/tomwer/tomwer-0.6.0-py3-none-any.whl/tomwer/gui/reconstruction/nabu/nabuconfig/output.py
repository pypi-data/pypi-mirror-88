# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2020 European Synchrotron Radiation Facility
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
__date__ = "11/02/2020"


import os
from silx.gui import qt
from tomwer.gui.reconstruction.nabu.nabuconfig.base import _NabuStageConfigBase
from tomwer.core.process.reconstruction.nabu.utils import _NabuStages
from silx.utils.enum import Enum as _Enum
import logging
from tomwer.io.utils import get_default_directory

try:
    import glymur
except ImportError:
    has_glymur = False
else:
    has_glymur = True

_logger = logging.getLogger(__name__)


class _NabuOutputFileFormat(_Enum):
    # NPY = 'npy'
    # NPZ = 'npz'
    TIFF = "tiff"
    HDF5 = "hdf5"
    JP2K = "jp2k"


class _NabuOutputConfig(_NabuStageConfigBase, qt.QWidget):
    """
    Widget to define the output configuration of nabu
    """

    sigConfChanged = qt.Signal(str)
    """Signal emitted when the configuration change. Parameter is the option
    modified
    """

    def __init__(self, parent):
        _NabuStageConfigBase.__init__(self, stage=_NabuStages.POST)
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())

        # output dir
        self._outputLabel = qt.QLabel("output:", self)
        self.layout().addWidget(self._outputLabel, 0, 0, 1, 1)
        self._defaultOutput = qt.QCheckBox("raw data root level", self)
        self._defaultOutput.setToolTip(
            "set reconstruction at the the same " "level as raw data"
        )
        self.layout().addWidget(self._defaultOutput, 0, 1, 1, 1)
        self._outputDirQLE = qt.QLineEdit("", self)
        self.layout().addWidget(self._outputDirQLE, 0, 2, 1, 1)
        style = qt.QApplication.style()
        icon_opendir = style.standardIcon(qt.QStyle.SP_DirOpenIcon)
        self._selectOutputPB = qt.QPushButton(icon_opendir, "", self)
        self._selectOutputPB.setIcon(icon_opendir)
        self._selectOutputPB.setToolTip("select output directory")
        self.layout().addWidget(self._selectOutputPB, 0, 3, 1, 1)
        # is required in nabu configuration file but tomwer wan't to force
        # it to be in expert mode
        self.registerWidget(self._defaultOutput, "advanced")
        self.registerWidget(self._outputLabel, "advanced")
        self.registerWidget(self._outputDirQLE, "advanced")
        self.registerWidget(self._selectOutputPB, "advanced")

        # file format
        self._outputFileFormatLabel = qt.QLabel("output file format:", self)
        self.layout().addWidget(self._outputFileFormatLabel, 1, 0, 1, 1)
        self._fileFormatCB = qt.QComboBox(self)
        for ff in _NabuOutputFileFormat:
            if ff is _NabuOutputFileFormat.JP2K:
                if not has_glymur:
                    _logger.warning(
                        "could not load jp2k format, glymur and OpenJPEG requested"
                    )
                else:
                    from glymur import version

                    if version.openjpeg_version < "2.3.0":
                        _logger.warning(
                            "You must have at least version 2.3.0 of OpenJPEG "
                            "in order to write jp2k images."
                        )
                    else:
                        self._fileFormatCB.addItem(ff.value)
            else:
                self._fileFormatCB.addItem(ff.value)
        self.layout().addWidget(self._fileFormatCB, 1, 2, 1, 2)
        self.registerWidget(self._outputFileFormatLabel, "required")
        self.registerWidget(self._fileFormatCB, "required")

        # file per group
        self._filePerGroupLabel = qt.QLabel("frame per group:", self)
        self.layout().addWidget(self._filePerGroupLabel, 2, 0, 1, 1)
        self._framePerGroup = qt.QSpinBox(self)
        self._framePerGroup.setMinimum(100)
        self._framePerGroup.setSingleStep(50)
        self._framePerGroup.setMaximum(10000)
        # not managed for now so hide
        self._filePerGroupLabel.hide()
        self._framePerGroup.hide()
        self.layout().addWidget(self._framePerGroup, 2, 2, 1, 2)

        # spacer for style
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer, 200, 0, 1, 1)

        # set up
        self._defaultOutput.setChecked(True)
        self._hideOutput(True)
        self.setFramePerGroup(100)
        self.setFileformat("hdf5")

        # connect signal / slot
        self._defaultOutput.toggled.connect(self._hideOutput)
        self._selectOutputPB.released.connect(self._selectOutput)
        self._outputDirQLE.editingFinished.connect(self._outputDirChanged)
        self._fileFormatCB.currentTextChanged.connect(self._fileFormatChanged)
        self._framePerGroup.valueChanged.connect(self._framePerGroupChanged)

    def _hideOutput(self, hide):
        self._outputDirQLE.setVisible(not hide)
        self._selectOutputPB.setVisible(not hide)

    def _selectOutput(self):
        defaultDirectory = self._outputDirQLE.text()
        if os.path.isdir(defaultDirectory):
            defaultDirectory = get_default_directory()

        dialog = qt.QFileDialog(self, directory=defaultDirectory)
        dialog.setFileMode(qt.QFileDialog.DirectoryOnly)

        if not dialog.exec_():
            dialog.close()
            return

        self._outputDirQLE.setText(dialog.selectedFiles()[0])

    def _outputDirChanged(self):
        self.sigConfChanged.emit("location")

    def _fileFormatChanged(self):
        self.sigConfChanged.emit("file_format")

    def _framePerGroupChanged(self):
        self.sigConfChanged.emit("frames_per_group")

    def getOutputDir(self):
        """

        :return: None if the default output directory is selected else
                 return path to the directory
        """
        if self._defaultOutput.isChecked():
            return None
        else:
            return self._outputDirQLE.text()

    def setOutputDir(self, dir):
        if dir in (None, ""):
            self._defaultOutput.setChecked(True)
        else:
            self._defaultOutput.setChecked(False)
            self._outputDirQLE.setText(dir)

    def getFileFormat(self) -> _NabuOutputFileFormat:
        return _NabuOutputFileFormat.from_value(self._fileFormatCB.currentText())

    def setFileformat(self, file_format):
        file_format = _NabuOutputFileFormat.from_value(file_format)
        index = self._fileFormatCB.findText(file_format.value)
        self._fileFormatCB.setCurrentIndex(index)

    def getFramePerGroup(self):
        return self._framePerGroup.value()

    def setFramePerGroup(self, n_frames):
        self._framePerGroup.setValue(n_frames)

    def getConfiguration(self):
        return {
            "file_format": self.getFileFormat().value,
            "location": self.getOutputDir() or "",
            # 'frames_per_group': self.getFramePerGroup(),
        }

    def setConfiguration(self, config):
        if "file_format" in config:
            self.setFileformat(config["file_format"])
        if "location" in config:
            self.setOutputDir(config["location"])
        if "frames_per_group" in config:
            self.setFramePerGroup(int(config["frames_per_group"]))


if __name__ == "__main__":
    app = qt.QApplication([])
    widget = _NabuOutputConfig(parent=None)
    widget.show()
    print(widget.getConfiguration())
    app.exec_()
