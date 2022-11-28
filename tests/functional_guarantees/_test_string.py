import unittest

from pyguarantees import functional_guarantees as fg


class TestStringGuarantee(unittest.TestCase):
    def test_basic(self):
        @fg.add_guarantees(param_guarantees=[fg.IsStr("a")])
        def fct(a):
            return a

        # Check allows correct type
        fct("Hi :)")

        # Check raises errors
        try:
            fct(1)
            self.assertTrue(False)   # should have raised exception
        except fg.exceptions.ParameterGuaranteesTypeError:
            self.assertTrue(True)    # successfully raised exception

    def test_force_conversion(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsStr("a", force_conversion=True)
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
        @fg.add_guarantees(param_guarantees=[
            fg.IsStr("a", minimum_len=2, maximum_len=5)
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
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)    # successfully raised exception

        try:
            fct("123456")
            self.assertTrue(False)   # should have raised exception
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)    # successfully raised exception

    def test_isin(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsStr("a", isin=["hi", "ciao"])
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
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)    # successfully raised exception

    def test_incorrect_guarantee_parameters_min(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsStr("a", minimum_len="nope")
        ])
        def fct(a):
            return a

        try:
            fct("hi")
            self.assertTrue(False)   # should have raised exception
        except fg.exceptions.FunctionalGuaranteesUserTypeError:
            self.assertTrue(True)    # successfully raised exception

    def test_incorrect_guarantee_parameters_max(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsStr("a", maximum_len="nope")
        ])
        def fct(a):
            return a

        try:
            fct("hi")
            self.assertTrue(False)  # should have raised exception
        except fg.exceptions.FunctionalGuaranteesUserTypeError:
            self.assertTrue(True)  # successfully raised exception

    def test_incorrect_guarantee_parameters_isin(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsStr("a", isin="nope")
        ])
        def fct(a):
            return a

        try:
            fct("hi")
            self.assertTrue(False)  # should have raised exception
        except fg.exceptions.FunctionalGuaranteesUserTypeError:
            self.assertTrue(True)  # successfully raised exception
