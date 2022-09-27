import unittest
from guarantees import functional_guarantees as fg


class TestReturnGuarantees(unittest.TestCase):
    def test_correct(self) -> None:
        @fg.add_guarantees(
            function_name="TestReturnGuarantees.test_correct.fct",
            function_namespace="_test_return_guarantees",
            return_guarantee=fg.IsInt("a"))
        def fct(a):
            return a

        ret_val = fct(1)
        self.assertIsInstance(ret_val, int)

    def test_false(self):
        @fg.add_guarantees(
            function_name="TestReturnGuarantees.test_false.fct",
            function_namespace="_test_return_guarantees",
            return_guarantee=fg.IsInt("a"))
        def fct(a):
            return float(a)

        try:
            fct(1)
            self.assertTrue(False)   # should have raised an exception
        except TypeError:
            self.assertTrue(True)    # successfully raised an exception

    def test_false_with_conversion(self):
        @fg.add_guarantees(
            function_name="TestReturnGuarantees.test_false_with_conversion.fct",
            function_namespace="_test_return_guarantees",
            return_guarantee=fg.IsInt("a", force_conversion=True))
        def fct(a):
            return float(a)

        ret_val = fct(1)
        self.assertIsInstance(ret_val, int)
