import unittest
import guarantees


class CbException(Exception):
    pass


class TestCallback(unittest.TestCase):
    def setUp(self) -> None:
        def cb(signal):
            raise CbException("success")

        self.cb = cb

    def test_isint_cb(self):
        @guarantees.parameter_guarantees([
            guarantees.IsInt("a", callback=self.cb)
        ])
        def fct(a):
            return a

        try:
            fct(1.)
            self.assertTrue(False)   # should have raised an exception
        except CbException:
            self.assertTrue(True)    # successfully raised exception

    def test_isstr_cb(self):
        @guarantees.parameter_guarantees([
            guarantees.IsStr("a", callback=self.cb)
        ])
        def fct(a):
            return a

        try:
            fct(1.)
            self.assertTrue(False)   # should have raised an exception
        except CbException:
            self.assertTrue(True)    # successfully raised exception

    def test_islist_cb(self):
        @guarantees.parameter_guarantees([
            guarantees.IsList("a", callback=self.cb)
        ])
        def fct(a):
            return a

        try:
            fct(1.)
            self.assertTrue(False)   # should have raised an exception
        except CbException:
            self.assertTrue(True)    # successfully raised exception



