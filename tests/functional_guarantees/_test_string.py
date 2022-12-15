import unittest

from pyguarantees import functional_guarantees as fg


class TestStringBasic(unittest.TestCase):
    def setUp(self):
        @fg.add_guarantees(param_guarantees=[fg.IsStr("a")])
        def fct(a):
            return a

        self.fct = fct

    def test_correct(self):
        self.fct("Hi :)")

    def test_violations(self):
        self.assertRaises(fg.exceptions.ParameterGuaranteesTypeError, self.fct, 1)


class TestStringForceConversion(unittest.TestCase):
    def test_correct(self):
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


class TestStringMinMaxLen(unittest.TestCase):
    def setUp(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsStr("a", minimum_len=2, maximum_len=5)
        ])
        def fct(a):
            return a

        self.fct = fct

    def test_correct(self):
        # Check correct inputs pass
        self.fct("12")
        self.fct("123")
        self.fct("1234")
        self.fct("12345")

    def test_violations(self):
        self.assertRaises(
            fg.exceptions.ParameterGuaranteesValueError,
            self.fct, "1"
        )
        self.assertRaises(
            fg.exceptions.ParameterGuaranteesValueError,
            self.fct, "123456"
        )


class TestStringIsIn(unittest.TestCase):
    def setUp(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsStr("a", isin=["hi", "ciao"])
        ])
        def fct(a):
            return a

        self.fct = fct

    def test_correct(self):
        self.fct("hi")
        self.fct("ciao")

    def test_violations(self):
        self.assertRaises(
            fg.exceptions.ParameterGuaranteesValueError,
            self.fct, "nope"
        )


class TestStringIncorrectParameters(unittest.TestCase):
    def test_min(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsStr("a", minimum_len="nope")
        ])
        def fct(a):
            return a

        self.assertRaises(
            fg.exceptions.FunctionalGuaranteesUserTypeError,
            fct, "hi"
        )

    def test_max(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsStr("a", maximum_len="nope")
        ])
        def fct(a):
            return a

        self.assertRaises(
            fg.exceptions.FunctionalGuaranteesUserTypeError,
            fct, "hi"
        )

    def test_isin(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsStr("a", isin="nope")
        ])
        def fct(a):
            return a

        self.assertRaises(
            fg.exceptions.FunctionalGuaranteesUserTypeError,
            fct, "hi"
        )
