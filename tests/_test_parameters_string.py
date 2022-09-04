import unittest

from guarantees import parameter_guarantees as pg


class TestStringGuarantee(unittest.TestCase):
    def test_basic(self):
        @pg.parameter_guarantees([
            pg.IsStr("a")
        ])
        def fct(a):
            return a

        # Check allows correct type
        fct("Hi :)")

        # Check raises errors
        try:
            fct(1)
            self.assertTrue(False)   # should have raised exception
        except TypeError:
            self.assertTrue(True)    # successfully raised exception

    def test_force_conversion(self):
        @pg.parameter_guarantees([
            pg.IsStr("a", force_conversion=True)
        ])
        def fct(a):
            return a

        # Check correct conversion
        s = fct(1)
        self.assertIs(type(s), str)
        s = fct(True)
        self.assertIs(type(s), str)
        s = fct([1, 2, 3])
        self.assertIs(type(s), str)

    def test_minmax_len(self):
        @pg.parameter_guarantees([
            pg.IsStr("a", minimum_len=2, maximum_len=5)
        ])
        def fct(a):
            return a

        # Check correct inputs pass
        fct("12")
        fct("123")
        fct("1234")
        fct("12345")

        # Check exceptions raised
        try:
            fct("1")
            self.assertTrue(False)   # should have raised exception
        except ValueError:
            self.assertTrue(True)    # successfully raised exception

        try:
            fct("123456")
            self.assertTrue(False)   # should have raised exception
        except ValueError:
            self.assertTrue(True)    # successfully raised exception

    def test_isin(self):
        @pg.parameter_guarantees([
            pg.IsStr("a", isin=["hi", "ciao"])
        ])
        def fct(a):
            return a

        # Check correct inputs work
        fct("hi")
        fct("ciao")

        # Check errors caught
        try:
            fct("nope")
            self.assertTrue(False)   # should have raised exception
        except ValueError:
            self.assertTrue(True)    # successfully raised exception

    def test_incorrect_guarantee_parameters_min(self):
        @pg.parameter_guarantees([
            pg.IsStr("a", minimum_len="nope")
        ])
        def fct(a):
            return a

        try:
            fct("hi")
            self.assertTrue(False)   # should have raised exception
        except TypeError:
            self.assertTrue(True)    # successfully raised exception

    def test_incorrect_guarantee_parameters_max(self):
        @pg.parameter_guarantees(([
            pg.IsStr("a", maximum_len="nope")
        ]))
        def fct(a):
            return a

        try:
            fct("hi")
            self.assertTrue(False)  # should have raised exception
        except TypeError:
            self.assertTrue(True)  # successfully raised exception

    def test_incorrect_guarantee_parameters_isin(self):
        @pg.parameter_guarantees(([
            pg.IsStr("a", isin="nope")
        ]))
        def fct(a):
            return a

        try:
            fct("hi")
            self.assertTrue(False)  # should have raised exception
        except TypeError:
            self.assertTrue(True)  # successfully raised exception
