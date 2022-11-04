import unittest

from guarantees.test_guarantees import exceptions
from ._decorators import fdata


class TestGuarantees(unittest.TestCase):
    def test_all_tests_implemented(self):
        failed_fcts = []
        for fct in fdata.keys():
            if fdata[fct]["num_tests"] == 0:
                failed_fcts.append(fct)

        if failed_fcts:
            raise exceptions.TestsNotImplementedError(failed_fcts)

    def test_functions_used_in_tests(self):
        failed_fcts = []
        for fct in fdata.keys():
            if fdata[fct]["usage_guaranteed"] and \
                    fdata[fct]["num_tests_with_calls"] < fdata[fct]["num_tests"]:
                failed_fcts.append(fct)

        if failed_fcts:
            raise exceptions.NotUsedInTestsError(failed_fcts)
