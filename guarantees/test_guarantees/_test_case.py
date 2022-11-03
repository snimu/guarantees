import unittest

from guarantees.test_guarantees import exceptions
from ._decorators import fdata


class TestGuarantees(unittest.TestCase):
    def test_all_tests_implemented(self):
        failed_fcts = []
        for fct in fdata.keys():
            if not fdata[fct]["has_test"]:
                failed_fcts.append(fct)

        if failed_fcts:
            raise exceptions.TestsNotImplementedError(failed_fcts)
