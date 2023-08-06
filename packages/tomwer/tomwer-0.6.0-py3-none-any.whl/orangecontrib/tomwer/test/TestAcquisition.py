# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2015-2016 European Synchrotron Radiation Facility
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
"""Full tomwer test suite.

"""

__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "19/01/2017"

import logging
import os
import shutil

from tomwer.core.scan.edfscan import EDFTomoScan
from silx.gui import qt

from tomwer.test.utils import UtilsTest

logger = logging.getLogger(__name__)


class Simulation(qt.QThread):
    """Simulation is a simple class able to simulate an acquisition by copying
    files on a targetted directory.

    :param str: targetdir the folder where the acquisition is stored
    :param str: manipulationId the id of the simulation we want to simulate
    :param str: finalState when launched, the state to reach before stopping

    :warning: the targetted directory won't be removed or cleaned during class
        destruction. This is to be managed by callers.
    """

    advancement = {
        "not started": -1,
        "starting-s0": 0,
        "starting-s1": 1,
        "acquisitionRunning": 2,
        "acquisitionDone": 3,
        "reconstructionLaunched": 4,
    }
    sigAdvancementChanged = qt.Signal(int)

    __definedDataset = ["test01", "test10"]

    def __init__(self, targetdir, manipulationId, finalState=4):
        assert type(manipulationId) is str
        assert type(targetdir) is str
        assert manipulationId in self.__definedDataset
        super(Simulation, self).__init__()

        self.targetdir = targetdir
        self.outputFolder = os.path.sep.join((targetdir, manipulationId))
        self.finalState = finalState
        self.currentState = "not started"
        self._createFinalXML = False
        (
            self.originalFolder,
            self.nbSlices,
            self.manipulationId,
        ) = self.__getOriginalDataSet(manipulationId)
        self.stopFileCreationForRunningState = int(self.nbSlices / 2)
        self.srcPattern = None
        self.destPattern = None

    def __getOriginalDataSet(self, dataSetID):
        """Return paths to the requested scan"""
        assert dataSetID in self.__definedDataset
        dataDir = UtilsTest.getEDFDataset(dataSetID)

        assert os.path.isdir(dataDir)
        assert os.path.isfile(os.path.join(dataDir, dataSetID + ".info"))
        slices = EDFTomoScan(dataDir).projections
        nbSlices = len(slices)
        manipulationID = dataSetID

        return dataDir, nbSlices, manipulationID

    def advanceTo(self, state):
        """Reset the new advancement targetted

        :param str state: the new state to reach when run will be executed
        """
        assert state in Simulation.advancement
        assert type(state) is str
        self.finalState = Simulation.advancement[state]

    def setSrcDestPatterns(self, srcPattern, destPattern):
        """
        If setted, will set the .info and .xml files into a different folder
        """
        self.srcPattern = srcPattern
        self.destPattern = destPattern
        if srcPattern is not None or destPattern is not None:
            assert os.path.isdir(srcPattern)
            assert os.path.isdir(destPattern)
            targettedFolder = self.outputFolder.replace(
                self.srcPattern, self.destPattern, 1
            )
            if not os.path.isdir(targettedFolder):
                os.mkdir(targettedFolder)

    def __shouldExecStep(self, step):
        """Return True if the thread should exec this step to advance taking
        into consideration is current state and his final state
        """
        return self.finalState >= self.advancement[step] and (
            Simulation.advancement[self.currentState] + 1 == self.advancement[step]
        )

    def run(self):
        """Main function, run the acquisition through all states until
        finalState is reached
        """
        if self.__shouldExecStep("starting-s0") is True:
            logger.info("starting-s0")
            self._startAcquisition()
            self.currentState = "starting-s0"
            self.signalCurrentState()

        if self.__shouldExecStep("starting-s1") is True:
            self.copyInitialFiles()
            logger.info("starting-s1")
            self.currentState = "starting-s1"
            self.signalCurrentState()

        if self.__shouldExecStep("acquisitionRunning") is True:
            self._copyScans((0, self.stopFileCreationForRunningState))
            logger.info("acquisitionRunning")
            self.currentState = "acquisitionRunning"
            self.signalCurrentState()

        if self.__shouldExecStep("acquisitionDone") is True:
            self._copyScans((self.stopFileCreationForRunningState, self.nbSlices))
            if self._createFinalXML is True:
                inputXMLFile = os.path.join(
                    self.originalFolder, self.manipulationId + ".xml"
                )
                assert os.path.isfile(inputXMLFile)
                ouputXMLFile = os.path.join(
                    self.outputFolder, self.manipulationId + ".xml"
                )
                shutil.copyfile(inputXMLFile, ouputXMLFile)

            logger.info("acquisitionDone")
            self.currentState = "acquisitionDone"
            self.signalCurrentState()

    def signalCurrentState(self):
        """Signal the actual state of the simulation"""
        self.sigAdvancementChanged.emit(self.currentState)

    def _startAcquisition(self):
        """create needed data dir"""
        for newFolder in (self.targetdir, self.outputFolder):
            if not os.path.exists(self.outputFolder):
                os.makedirs(self.outputFolder)

    def _copyScans(self, _slicesRange):
        """copy the .edf file from the original directory to the outputFolder

        :_slicesRange tuple: the _range of slices data we want to copy
        """
        logger.info("copying files from %s to %s" % (_slicesRange[0], _slicesRange[1]))
        for iSlice in list(range(_slicesRange[0], _slicesRange[1])):
            filename = "".join((self.manipulationId, format(iSlice, "04d"), ".edf"))
            srcFile = os.path.join(self.originalFolder, filename)
            outputFile = os.path.join(self.outputFolder, filename)
            assert os.path.isfile(srcFile)
            assert os.path.isdir(self.outputFolder)
            shutil.copyfile(srcFile, outputFile)

    def copyInitialFiles(self):
        """copy the .info file"""
        assert os.path.isdir(self.originalFolder)
        logger.info(
            "copying initial files (.info, .xml...) from %s to %s"
            % (self.originalFolder, self.manipulationId)
        )
        for extension in (".info", ".db", ".cfg"):
            filename = "".join((self.manipulationId, extension))
            srcFile = os.path.join(self.originalFolder, filename)

            targettedFolder = self.outputFolder
            if self.srcPattern is not None or self.destPattern is not None:
                targettedFolder = self.outputFolder.replace(
                    self.srcPattern, self.destPattern, 1
                )
            assert os.path.isfile(srcFile)
            assert os.path.isdir(targettedFolder)
            assert os.path.isdir(self.originalFolder)
            shutil.copy2(srcFile, targettedFolder)

    def createFinalXML(self, val):
        """If activated, once all the file will be copied, this will create
        an .xml file into the output directory
        """
        self._createFinalXML = val

    def createParFile(self):
        pass

    def createReconstructedFile(self):
        pass

    def createOARJob(self):
        pass

    def createDark(self):
        pass

    def createJPG(self):
        pass

    def createVolfloat(self):
        pass

    def createVolraw(self):
        pass

    def __createFileTo(self, filePath):
        assert type(filePath) is str
        open(filePath, "a").close()


def main():
    import time

    _qapp = qt.QApplication.instance() or qt.QApplication([])

    inputdir = "/tmp"
    manipulationId = "test10"
    s = Simulation(
        inputdir,
        manipulationId,
        finalState=Simulation.advancement["acquisitionRunning"],
    )
    s.start()
    while not s.isFinished():
        _qapp.processEvents()
        time.sleep(1)


if __name__ == "__main__":
    main()
