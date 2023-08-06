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
__date__ = "05/07/2017"


import os
import shutil
import fnmatch
from tomwer.core.process.baseprocess import SingleProcess, _input_desc, _output_desc
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.settings import get_lbsram_path, get_dest_path
from tomwer.core.signal import Signal
from tomwer.core.utils import logconfig, rebaseParFile
import logging
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.hdf5scan import HDF5TomoScan
import tomwer.version

logger = logging.getLogger(__name__)

try:
    from tomwer.synctools.rsyncmanager import RSyncManager
except ImportError:
    logger.warning("rsyncmanager not available")
    has_rsync = False
else:
    has_rsync = True


class FolderTransfert(SingleProcess):
    """Manage the copy of scan.

    .. warning : the destination directory is find out from the file system
                 if /lbsramxxx exists for example...
                 In the case we couldn't found the output directory then we
                 will ask for the user to set it.
    """

    inputs = [
        _input_desc(
            name="data", type=TomwerScanBase, handler="process", doc="scan path"
        )
    ]
    outputs = [_output_desc(name="data", type=TomwerScanBase, doc="scan path")]

    scanready = Signal(TomwerScanBase)

    def __init__(self):
        SingleProcess.__init__(self)
        self.turn_off_print = False
        self._destDir = None
        """
        output directory if forced. By default based by the env variable
        'TARGET_OUTPUT_FOLDER' if exists, else set to '/data/visitor'
         """
        self._copying = False
        self._block = False

    def set_properties(self, properties):
        # No properties stored for now
        if "dest_dir" in properties:
            self.setDestDir(properties["dest_dir"])

    @staticmethod
    def program_name():
        """Name of the program used for this processing"""
        return "data transfer"

    @staticmethod
    def program_version():
        """version of the program used for this processing"""
        return tomwer.version.version

    @staticmethod
    def definition():
        """definition of the process"""
        return "transfer data from a folder to another"

    def _getDefaultOutputDir(self):
        """Return the default output dir based on the computer setup"""
        if "TARGET_OUTPUT_FOLDER" in os.environ:
            return os.environ["TARGET_OUTPUT_FOLDER"]

        if os.path.isdir("/data/visitor"):
            return "/data/visitor"

        return ""

    def _process_edf_scan(self, scan, move=False, force=True, noRsync=False):
        assert isinstance(scan, EDFTomoScan)
        outputdir = self.getDestinationDir(scan.path)
        if outputdir is None:
            return

        self._pretransfertOperations(scan.path, outputdir)
        # as we are in the workflow we want this function to be bloking.
        # so we will not used a thread for folder synchronization
        # for now rsync is not delaing with force option
        if not has_rsync or noRsync is True or RSyncManager().has_rsync() is False:
            logger.info("Can't use rsync, copying files")
            try:
                if move is True:
                    self._moveFiles(
                        scanPath=scan.path,
                        outputdir=os.path.dirname(outputdir),
                        force=force,
                    )
                else:
                    self._copyFiles(
                        scanPath=scan.path, outputdir=outputdir, force=force
                    )
            except shutil.Error as e:
                raise e
            else:
                if isinstance(scan, HDF5TomoScan):
                    _entry = scan.entry
                else:
                    _entry = None
                output_scan = scan._deduce_transfert_scan(outputdir)
                try:
                    output_scan._update_latest_recons_urls(
                        old_path=scan.path, new_path=output_scan.path
                    )
                except Exception as e:
                    logger.warning(
                        "Fail to convert url of latest reconstruction. Reason is:" + e
                    )
                    output_scan.clear_latest_reconstructions()
                self.__noticeTransfertSuccess(input_scan=scan, output_scan=output_scan)
        else:
            source = scan.path
            if not source.endswith(os.path.sep):
                source = source + os.path.sep
            target = outputdir

            if not target.endswith(os.path.sep):
                target = target + os.path.sep

            self._signalCopying(scanID=source, outputdir=target)
            output_scan = scan._deduce_transfert_scan(outputdir)
            try:
                output_scan._update_latest_recons_urls(
                    old_path=scan.path, new_path=output_scan.path
                )
            except Exception as e:
                logger.warning(
                    "Fail to convert url of latest reconstruction. Reason is:" + e
                )
                output_scan.clear_latest_reconstructions()
            RSyncManager().sync_file(
                source=source,
                target=target,
                wait=self._block,
                delete=True,
                callback=self.__noticeTransfertSuccess,
                callback_parameters=(scan, output_scan),
                rights=777,
            )

        self.register_output(key="data", value=outputdir)

    def _get_hdf5_dst_scan(self, bliss_scan_folder_path):
        if self._destDir is not None:
            rel_path = os.path.join(*bliss_scan_folder_path.split(os.sep)[-2:])
            return os.path.dirname(os.path.join(self._destDir, rel_path))
        # try to get outputdir from spec
        scanIDPath = os.path.abspath(bliss_scan_folder_path)
        return self._getOutputDirSpec() or os.path.join(
            *self._getOutputDirLBS(scanIDPath).split(os.sep)[:-1]
        )

    def _get_hdf5_sample_file_or_nx_dst(self, bliss_sample_file):
        if self._destDir is not None:
            rel_path = os.path.join(*bliss_sample_file.split(os.sep)[-2:])
            return os.path.join(self._destDir, rel_path)
        # try to get outputdir from spec
        bliss_sample_file = os.path.abspath(bliss_sample_file)
        return self._getOutputDirSpec() or self._getOutputDirLBS(bliss_sample_file)

    def _get_master_sample_file_dst(self, master_sample_file):
        if self._destDir is not None:
            rel_path = os.path.join(*master_sample_file.split(os.sep)[-2:])
            return os.path.join(self._destDir, rel_path)
        # try to get outputdir from spec
        master_sample_file = os.path.abspath(master_sample_file)
        return self._getOutputDirSpec() or self._getOutputDirLBS(master_sample_file)

    def _get_hdf5_proposal_file_dst(self, bliss_proposal_file):
        if self._destDir is not None:
            return os.path.join(self._destDir, os.path.split(bliss_proposal_file)[-1])
        # try to get outputdir from spec
        bliss_sample_file = os.path.abspath(bliss_proposal_file)
        return self._getOutputDirSpec() or self._getOutputDirLBS(bliss_sample_file)

    def _process_hdf5_scan(self, scan):
        assert isinstance(scan, HDF5TomoScan)
        from tomwer.core.process.control.datalistener import DataListener

        files_sources = []
        files_dest = []
        delete_opt = []

        if os.path.exists(scan.process_file):
            source_scans = DataListener.get_source_scans(
                process_file=scan.process_file, entry=scan.entry
            )
        else:
            source_scans = None
        # manage scan folder
        if source_scans is not None:
            for source_scan in source_scans:
                files_sources.append(source_scan)
                files_dest.append(
                    self._get_hdf5_dst_scan(bliss_scan_folder_path=source_scan)
                )
                delete_opt.append(True)

        # manage proposal file
        if os.path.exists(scan.process_file):
            proposal_file = DataListener.get_proposal_file(
                process_file=scan.process_file, entry=scan.entry
            )
        else:
            proposal_file = None
        if proposal_file is not None:
            files_sources.append(proposal_file)
            files_dest.append(self._get_hdf5_proposal_file_dst(proposal_file))
            delete_opt.append(False)

        # manage sample file
        if os.path.exists(scan.process_file):
            sample_file = DataListener.get_sample_file(
                process_file=scan.process_file, entry=scan.entry
            )

        else:
            sample_file = None
        if sample_file is not None:
            files_sources.append(sample_file)
            files_dest.append(self._get_hdf5_sample_file_or_nx_dst(sample_file))
            delete_opt.append(False)

        # manage saving file
        if os.path.exists(scan.process_file):
            mst_sample_file = DataListener.get_master_sample_file(
                process_file=scan.process_file, entry=scan.entry
            )
        else:
            mst_sample_file = None
        if mst_sample_file is not None:
            files_sources.append(mst_sample_file)
            files_dest.append(self._get_master_sample_file_dst(mst_sample_file))
            delete_opt.append(False)

        # manage .nx file
        if os.path.exists(scan.master_file):
            files_sources.append(scan.master_file)
            new_nx_file = self._get_hdf5_sample_file_or_nx_dst(scan.master_file)
            files_dest.append(new_nx_file)
            delete_opt.append(True)
            output_scan = HDF5TomoScan(scan=new_nx_file, entry=scan.entry)
        else:
            output_scan = None

        # manage files generated (*slice*.h5/edf, *.cfg, *.par...)
        # for reconstructed file, .h5, .edf if there is some conflict at one
        # point I guess we might need to check file entry ? or rename the file
        # according to the entry.

        patterns = ["*.par", "*.cfg", "*.rec"]
        # manage .par, .cfg and .rec files if any
        patterns += ["*slice*.hdf5", "*slice*.h5", "*slice*.edf"]
        # manage *slice*.hdf5 and *slice*.edf files (reconstructed slice)
        patterns += ["tomwer_processes.h5"]

        def match_pattern(file_name):
            file_name = file_name.lower()
            for pattern in patterns:
                if fnmatch.fnmatch(file_name, pattern):
                    return True
            return False

        dir_name = os.path.dirname(scan.master_file)
        for file_ in os.listdir(dir_name):
            if match_pattern(file_name=file_):
                full_file_path = os.path.join(dir_name, file_)
                files_sources.append(full_file_path)
                files_dest.append(self._get_hdf5_sample_file_or_nx_dst(full_file_path))
                delete_opt.append(True)

        RSyncManager().sync_files(
            sources=files_sources,
            targets=files_dest,
            wait=self._block,
            delete=delete_opt,
            callback=self.__noticeTransfertSuccess,
            callback_parameters=(scan, output_scan),
        )

    def process(self, scan, move=False, force=False, noRsync=False):
        """Launch the process process

        :param scan: the path to the file we want to move/process
        :type scan: :class:`.TomoBase`
        :param move: if True, directly move the files. Otherwise copy the files
        :param force: if True then force the copy even if the file/folder already
            exists
        :param bool noRSync: True if we wan't do sue shutil instead of rsync.
        """
        if scan is None:
            return

        _scan = scan
        if type(_scan) is dict:
            _scan = ScanFactory.create_scan_object_frm_dict(scan)

        assert isinstance(_scan, TomwerScanBase)
        assert move in (True, False)

        logger.info("synchronisation with scanPath")
        if isinstance(scan, EDFTomoScan):
            self._process_edf_scan(scan=scan, move=move, force=force, noRsync=noRsync)
        elif isinstance(scan, HDF5TomoScan):
            if move is True:
                raise NotImplementedError("move option not implemented")
            if noRsync is True:
                raise NotImplementedError("noRsync option not implemented")

            self._process_hdf5_scan(scan=scan)
        else:
            raise TypeError("Other scan than EDF or HDF5 are not managed")

        if self._return_dict:
            return _scan.to_dict()
        else:
            return _scan

    def _pretransfertOperations(self, scanfolder, outputdir):
        """Operation to be run before making the transfert of the scan"""
        self._updateParFiles(scanfolder, outputdir)

    def _updateParFiles(self, scanfolder, outputdir):
        """Update all path contained in the .par files to fit the new outpudir"""
        for _file in os.listdir(scanfolder):
            if _file.lower().endswith(".par"):
                rebaseParFile(
                    os.path.join(scanfolder, _file),
                    oldfolder=scanfolder,
                    newfolder=outputdir,
                )

    def __noticeTransfertSuccess(self, input_scan, output_scan):
        self._signalCopySucceed()

        results = {"input_scan": str(input_scan), "output_scan": str(output_scan)}
        entry = "entry"
        if isinstance(output_scan, HDF5TomoScan):
            entry = output_scan.entry
        self.register_process(
            process_file=output_scan.process_file,
            entry=entry,
            results=results,
            process_index=output_scan.pop_process_index(),
            configuration=None,
        )
        logger.processSucceed(
            "transfer succeed of {} to {}".format(str(input_scan), str(output_scan)),
            extra={
                logconfig.DOC_TITLE: self._scheme_title,
                logconfig.FROM: str(input_scan),
                logconfig.TO: str(output_scan),
            },
        )
        self.signalTransfertOk(input_scan=input_scan, output_scan=output_scan)

    def signalTransfertOk(self, input_scan, output_scan):
        if input_scan is None or output_scan is None:
            return
        assert isinstance(input_scan, TomwerScanBase)
        assert isinstance(output_scan, TomwerScanBase)
        self.scanready.emit(output_scan)

    def _copyFiles(self, scanPath, outputdir, force):
        """Copying files and removing them"""
        assert type(scanPath) is str
        assert type(outputdir) is str
        assert os.path.isdir(scanPath)
        #        if force is False:
        #            assert(os.path.isdir(outputdir))
        # create the destination dir
        if not os.path.isdir(outputdir):

            def createDirAndTopDir(_dir):
                if not os.path.isdir(os.path.dirname(_dir)):
                    createDirAndTopDir(os.path.dirname(_dir))
                os.mkdir(_dir)

            createDirAndTopDir(outputdir)
        # we can't copy directly the top folder because he is already existing
        for f in os.listdir(scanPath):
            file = os.path.join(scanPath, f)
            fileDest = os.path.join(outputdir, f)
            if force is True:
                if os.path.isdir(fileDest):
                    shutil.rmtree(fileDest)
                if os.path.isfile(fileDest):
                    os.remove(fileDest)
            if os.path.exists(fileDest):
                raise FileExistsError(fileDest, "already exists")
            if os.path.isdir(file):
                shutil.copytree(src=file, dst=fileDest)
            else:
                shutil.copy2(src=file, dst=fileDest)

        info = "Removing directory at %s" % scanPath
        logger.info(info)
        shutil.rmtree(scanPath)
        info = "sucessfuly removed file at %s !!!" % scanPath
        logger.info(info)

    def _moveFiles(self, scanPath, outputdir, force):
        """Function simply moving files"""
        assert os.path.isdir(scanPath)
        if force is False:
            assert os.path.isdir(outputdir)

        logger.debug(
            "synchronisation with scanPath",
            extra={logconfig.DOC_TITLE: self._scheme_title},
        )

        target = os.path.join(outputdir, os.path.basename(scanPath))
        if force is True and os.path.isdir(target):
            shutil.rmtree(target)
        shutil.move(scanPath, outputdir)

    def _requestFolder(self):
        out = None
        while out is None:
            out = input("please give the output directory : \n")
            if not os.path.isdir(out):
                warning = "given path " + out
                warning += " is not a directory, please give a valid directory"
                logger.warning(warning)
                out = None
        return out

    def _getOutputDirSpec(self):
        return None

    def _getOutputDirLBS(self, scanPath):
        if scanPath.startswith(get_lbsram_path()):
            return scanPath.replace(get_lbsram_path(), get_dest_path(), 1)
        else:
            return None

    def getDestinationDir(self, scanPath):
        """Return the destination directory. The destination directory is the
        root directory"""
        if self._destDir is not None:
            return os.path.join(self._destDir, os.path.basename(scanPath))

        # try to get outputdir from spec
        scanIDPath = os.path.abspath(scanPath)

        outputdir = self._getOutputDirSpec() or self._getOutputDirLBS(scanIDPath)
        if outputdir is None:
            outputdir = self._requestFolder()

        return outputdir

    def setDestDir(self, dist):
        """Force the outpudir to dist.

        :param str dist: path to the folder. If None remove force behavior
        """
        self._destDir = dist
        if self._destDir is not None and os.path.isdir(self._destDir):
            logger.warning("Given path %s is not a directory" % self._destDir)

    # some function to print the output in the terminal #

    def _signalCopying(self, scanID, outputdir):
        self._copying = True
        if self.turn_off_print is False:
            print("######################################")
            print("###")
            print("###")
            print("### copying files ", scanID, " to ", outputdir)
            print("### ...")

        info = "start moving folder from %s to %s" % (scanID, outputdir)
        logger.processStarted(info, extra={logconfig.DOC_TITLE: self._scheme_title})

    def _signalCopyFailed(self):
        self._copying = False
        if self.turn_off_print is False:
            print("###")
            print("### copy failed")
            print("###")
            print("######################################")

    def _signalCopySucceed(self):
        self._copying = False
        if self.turn_off_print is False:
            print("###")
            print("### copy succeeded")
            print("###")
            print("######################################")

    def isCopying(self):
        """

        :return: True if the folder transfert is actually doing a copy
        """
        return self._copying

    def setForceSync(self, b):
        """

        :param bool b: if True then folderTransfert will wait until transfert
            is done to be released. Otherwise will launch a 'free' thread wich
            will notice transfert end later.
        """
        self._block = b

    def getOutput(self, scan):
        """

        :param scan:
        :return:
        """
        return os.path.join(self.getDestinationDir(scan), os.path.basename(scan))
