import unittest
from guarantees import functional_guarantees as fg


class TestReturnGuarantees(unittest.TestCase):
    def test_correct(self) -> None:
        @fg.return_guarantees(fg.IsInt("a"))
        def fct(a):
            return a

        ret_val = fct(1)
        self.assertIsInstance(ret_val, int)

    def test_false(self):
        @fg.return_guarantees(fg.IsInt("a"))
        def fct(a):
            return float(a)

        try:
            fct(1)
            self.assertTrue(False)   # should have raised an exception
        except TypeError:
            self.assertTrue(True)    # successfully raised an exception

    def test_false_with_conversion(self):
        @fg.return_guarantees(fg.IsInt("a", force_conversion=True))
        def fct(a):
            return float(a)

        ret_val = fct(1)
        self.assertIsInstance(ret_val, int)
