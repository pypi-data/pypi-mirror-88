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

__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "16/09/2019"

import unittest

from ..process.test import suite as process_suite
from ..scan.test import suite as scan_suite
from . import test_tomo_workflow
from . import test_utils
from . import test_lamino
from . import test_scanutils


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(process_suite())
    test_suite.addTest(scan_suite())
    test_suite.addTest(test_tomo_workflow.suite())
    test_suite.addTest(test_utils.suite())
    test_suite.addTest(test_scanutils.suite())
    test_suite.addTest(test_lamino.suite())

    return test_suite
