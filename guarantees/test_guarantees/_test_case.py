import unittest
import exceptions


class TestGuaranteedTestsAreImplemented(unittest.TestCase):
    def test_all_tests_implemented(self):
        if len(fdata) == 0:
            return

        failed_fcts = []
        for fct, info in fdata.items():
            if not info["has_test"]:
                failed_fcts.append(fct)

        if failed_fcts:
            raise exceptions.TestsNotImplementedError(failed_fcts)


class TestUsedInTests(unittest.TestCase):
    def test_guaranteed_fcts_are_used(self):
        if len(fdata) == 0:
            return

        failed_fcts = []
        for fct, info in fdata.items():
            if info["has_test"] and not info["was_called"]:
                failed_fcts.append(fct)

        if failed_fcts:
            raise exceptions.NotUsedInTestsError(failed_fcts)
