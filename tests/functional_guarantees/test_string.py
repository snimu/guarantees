import pytest
from pyguarantees import functional_guarantees as fg


@fg.add_guarantees(param_guarantees=[fg.IsStr("a")])
def fct_base(a):
    return a


class TestStringBasic:
    def test_correct(self):
        fct_base("Hi :)")

    def test_violations(self):
        with pytest.raises(fg.exceptions.ParameterGuaranteesTypeError):
            fct_base(1)


class TestStringForceConversion:
    def test_correct(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsStr("a", force_conversion=True)
        ])
        def fct(a):
            return a

        # Check correct conversion
        s = fct(1)
        assert type(s) is str
        s = fct(True)
        assert type(s) is str
        s = fct([1, 2, 3])
        assert type(s) is str


@fg.add_guarantees(param_guarantees=[
    fg.IsStr("a", minimum_len=2, maximum_len=5)
])
def fct_minmax_len(a):
    return a


class TestStringMinMaxLen:
    def test_correct(self):
        fct_minmax_len("12")
        fct_minmax_len("123")
        fct_minmax_len("1234")
        fct_minmax_len("12345")

    def test_violations(self):
        with pytest.raises(fg.exceptions.ParameterGuaranteesValueError):
            fct_minmax_len("1")
        with pytest.raises(fg.exceptions.ParameterGuaranteesValueError):
            fct_minmax_len("123456")


@fg.add_guarantees(param_guarantees=[
    fg.IsStr("a", isin=["hi", "ciao"])
])
def fct_isin(a):
    return a


class TestStringIsIn:
    def test_correct(self):
        fct_isin("hi")
        fct_isin("ciao")

    def test_violations(self):
        with pytest.raises(fg.exceptions.ParameterGuaranteesValueError):
            fct_isin("nope")


class TestStringIncorrectParameters:
    def test_min(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsStr("a", minimum_len="nope")
        ])
        def fct(a):
            return a

        with pytest.raises(fg.exceptions.FunctionalGuaranteesUserTypeError):
            fct("hi")

    def test_max(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsStr("a", maximum_len="nope")
        ])
        def fct(a):
            return a

        with pytest.raises(fg.exceptions.FunctionalGuaranteesUserTypeError):
            fct("hi")

    def test_isin(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsStr("a", isin="nope")
        ])
        def fct(a):
            return a

        with pytest.raises(fg.exceptions.FunctionalGuaranteesUserTypeError):
            fct("hi")