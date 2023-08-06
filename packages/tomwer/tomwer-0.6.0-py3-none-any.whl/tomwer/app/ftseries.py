#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
from silx.gui import qt
import argparse
from tomwer.gui import icons
from tomwer.gui.utils.splashscreen import getMainSplashScreen
from tomwer.gui.reconstruction.ftserie import FtserieWidget
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.core.scan.scanfactory import ScanFactory
import signal

logging.basicConfig()
_logger = logging.getLogger(__name__)


def getinputinfo():
    return "tomwer ftseries [scan_path]"


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


def main(argv):
    import os

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "scan_path", help="Data file to show (h5 file, edf files, spec files)"
    )
    parser.add_argument(
        "--entry", default=None, help="An entry can be specify for hdf5 files"
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Set logging system in debug mode",
    )
    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        default=False,
        help="Only create the .par file and print the command executed",
    )
    options = parser.parse_args(argv[1:])

    global app  # QApplication must be global to avoid seg fault on quit
    app = qt.QApplication.instance() or qt.QApplication([])

    qt.QLocale.setDefault(qt.QLocale(qt.QLocale.English))
    qt.QLocale.setDefault(qt.QLocale.c())
    signal.signal(signal.SIGINT, sigintHandler)
    sys.excepthook = qt.exceptionHandler
    timer = qt.QTimer()
    timer.start(500)
    # Application have to wake up Python interpreter, else SIGINT is not
    # catch
    timer.timeout.connect(lambda: None)

    splash = getMainSplashScreen()
    options.scan_path = options.scan_path.rstrip(os.path.sep)
    if options.entry is not None:
        valid_entries = HDF5TomoScan.get_valid_entries(options.scan_path)
        if options.entry not in valid_entries:
            raise ValueError(
                "entry {} is invalid. Does it exists ? Is the "
                "file NXTomo compliant ?. Valid entry are {}"
                "".format(options.entry, valid_entries)
            )
        scan = HDF5TomoScan(scan=options.scan_path, entry=options.entry)
    else:
        scan = ScanFactory.create_scan_object(scan_path=options.scan_path)
    scan.set_process_index_frm_tomwer_process_file()

    widget = FtserieWidget()
    widget.setScan(scan=scan)
    # for the application we run for the reconstruction to be finished
    # to give back hand to the user
    widget.reconsStack._forceSync = True

    widget.set_dry_run(options.dry_run)
    widget.setWindowTitle("FtSerie")
    widget.setWindowIcon(icons.getQIcon("tomwer"))
    splash.finish(widget)
    widget.show()
    app.exec_()


if __name__ == "__main__":
    main(sys.argv)
