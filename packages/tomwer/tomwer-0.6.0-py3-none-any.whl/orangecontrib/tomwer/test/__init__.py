# coding: utf-8
# /*##########################################################################
# Copyright (C) 2016 European Synchrotron Radiation Facility
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
#############################################################################*/


__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "15/05/2017"

import unittest
from . import test_axis_reconstruction
from . import test_scanlist_samplemoved
from . import test_scanlist_ftserie
from . import test_dark_flat_field
from . import test_lamino
from . import test_nabu
from . import test_owidgets
from . import test_dump_widget_canvas
from . import test_folder_transfert
from . import test_workflow_volume
from ..widgets import test as test_widgets


def suite(loader=None, pattern="test*.py"):
    test_suite = unittest.TestSuite()
    test_suite.addTest(test_axis_reconstruction.suite())
    test_suite.addTest(test_widgets.suite())
    test_suite.addTest(test_scanlist_ftserie.suite())
    test_suite.addTest(test_dark_flat_field.suite())
    test_suite.addTest(test_lamino.suite())
    test_suite.addTest(test_nabu.suite())
    test_suite.addTest(test_scanlist_samplemoved.suite())
    test_suite.addTest(test_owidgets.suite())
    test_suite.addTest(test_dump_widget_canvas.suite())
    test_suite.addTests(test_folder_transfert.suite())
    test_suite.addTests(test_widgets.suite())
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
