import pytest
import pyguarantees as pg
from pyguarantees.constraints import IsStr, DynamicCheck


@pg.constrain.parameters(a=IsStr())
def fct_base(a):
    return a


class TestStringBasic:
    def test_correct(self):
        fct_base("Hi :)")

    def test_violations(self):
        with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesTypeError):
            fct_base(1)


class TestStringForceConversion:
    def test_correct(self):
        @pg.constrain.parameters(a=IsStr(force_conversion=True))
        def fct(a):
            return a

        # Check correct conversion
        s = fct(1)
        assert type(s) is str
        s = fct(True)
        assert type(s) is str
        s = fct([1, 2, 3])
        assert type(s) is str


@pg.constrain.parameters(a=IsStr(minimum_len=2, maximum_len=5))
def fct_minmax_len(a):
    return a


class TestStringMinMaxLen:
    def test_correct(self):
        fct_minmax_len("12")
        fct_minmax_len("123")
        fct_minmax_len("1234")
        fct_minmax_len("12345")

    def test_violations(self):
        with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesValueError):
            fct_minmax_len("1")
        with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesValueError):
            fct_minmax_len("123456")


@pg.constrain.parameters(a=IsStr(isin=["hi", "ciao"]))
def fct_isin(a):
    return a


class TestStringIsIn:
    def test_correct(self):
        fct_isin("hi")
        fct_isin("ciao")

    def test_violations(self):
        with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesValueError):
            fct_isin("nope")


@pg.constrain.parameters(a=IsStr(forbidden_values=["chocolate", "cookies"]))
def fct_no_sweets(a):
    return a


class TestStringForbiddenValues:
    def test_correct(self):
        fct_no_sweets("kale")
        fct_no_sweets("carrots")

    def test_violation(self):
        with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesValueError):
            fct_no_sweets("cookies")


@pg.constrain.parameters(a=IsStr(dynamic_checks=[DynamicCheck(check=lambda x: x.endswith(".pdf"))]))
def fct_dynamic_checks(a):
    return a


class TestStringDynamicChecks:
    def test_correct(self):
        fct_dynamic_checks("file1.pdf")
        fct_dynamic_checks("file2.kkk.eee.www.pdf")

    def test_violations(self):
        with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesValueError):
            fct_dynamic_checks("totallynotavirus.exe")


class TestStringIncorrectParameters:
    def test_min(self):
        @pg.constrain.parameters(a=IsStr(minimum_len="nope"))
        def fct(a):
            return a

        with pytest.raises(pg.exceptions.constraints.FunctionalGuaranteesUserTypeError):
            fct("hi")

    def test_max(self):
        @pg.constrain.parameters(a=IsStr(maximum_len="nope"))
        def fct(a):
            return a

        with pytest.raises(pg.exceptions.constraints.FunctionalGuaranteesUserTypeError):
            fct("hi")

    def test_mingemax(self):
        @pg.constrain.parameters(a=IsStr(minimum_len=5, maximum_len=1))
        def fct(a):
            return a

        with pytest.raises(pg.exceptions.constraints.FunctionalGuaranteesUserValueError):
            fct("hi")

    def test_isin(self):
        @pg.constrain.parameters(a=IsStr(isin="nope"))
        def fct(a):
            return a

        with pytest.raises(pg.exceptions.constraints.FunctionalGuaranteesUserTypeError):
            fct("hi")
