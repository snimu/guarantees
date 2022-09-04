import unittest
from guarantees import parameter_guarantees as pg


class TestReturnGuarantees(unittest.TestCase):
    def test_correct(self) -> None:
        @pg.return_guarantees(pg.IsInt("a"))
        def fct(a):
            return a

        ret_val = fct(1)
        self.assertIsInstance(ret_val, int)

    def test_false(self):
        @pg.return_guarantees(pg.IsInt("a"))
        def fct(a):
            return float(a)

        try:
            fct(1)
            self.assertTrue(False)   # should have raised an exception
        except TypeError:
            self.assertTrue(True)    # successfully raised an exception

    def test_false_with_conversion(self):
        @pg.return_guarantees(pg.IsInt("a", force_conversion=True))
        def fct(a):
            return float(a)

        ret_val = fct(1)
        self.assertIsInstance(ret_val, int)
