import unittest
from guarantees import functional_guarantees as fg


class CbException(Exception):
    pass


class TestCallback(unittest.TestCase):
    def setUp(self) -> None:
        def cb(signal):
            raise CbException("success")

        self.cb = cb

    def test_isint_cb(self):
        @fg.parameter_guarantees([
            fg.IsInt("a", error_callback=self.cb)
        ])
        def fct(a):
            return a

        try:
            fct(1.)
            self.assertTrue(False)   # should have raised an exception
        except CbException:
            self.assertTrue(True)    # successfully raised exception

    def test_isstr_cb(self):
        @fg.parameter_guarantees([
            fg.IsStr("a", error_callback=self.cb)
        ])
        def fct(a):
            return a

        try:
            fct(1.)
            self.assertTrue(False)   # should have raised an exception
        except CbException:
            self.assertTrue(True)    # successfully raised exception

    def test_islist_cb(self):
        @fg.parameter_guarantees([
            fg.IsList("a", error_callback=self.cb)
        ])
        def fct(a):
            return a

        try:
            fct(1.)
            self.assertTrue(False)   # should have raised an exception
        except CbException:
            self.assertTrue(True)    # successfully raised exception


class TestOnOff(unittest.TestCase):
    def test_onoff(self):
        @fg.parameter_guarantees([
            fg.IsInt("a")
        ])
        def fct(a):
            return a

        # Check that it works in general
        val = fct(1)
        self.assertIsInstance(val, int)

        try:
            fct("not an int!")
            self.assertTrue(False)
        except TypeError:
            self.assertTrue(True)

        fg.off()
        fct("not an int!")

        fg.on()
        try:
            fct("not an int!")
            self.assertTrue(False)
        except TypeError:
            self.assertTrue(True)


def test_onoff():
    """TestOnOff cannot be run as part of unittest.main(), because all tests
    are run in parallel and guarantees.off() would impact all other tests.
    Therefore, provide this function to be run before or after running
    unittest.main()."""
    suite = unittest.TestSuite()
    suite.addTest(TestOnOff())
    runner = unittest.TextTestRunner()
    runner.run(suite)
