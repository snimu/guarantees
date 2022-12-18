import pytest

import pyguarantees as pg
from pyguarantees.constraints import IsInt, IsStr


class TestReturnGuarantees:
    def test_correct(self) -> None:
        @pg.constrain.returns(IsInt())
        def fct(a):
            return a

        ret_val = fct(1)
        assert isinstance(ret_val, int)

    def test_false(self):
        @pg.constrain.returns(IsInt())
        def fct(a):
            return float(a)

        with pytest.raises(pg.exceptions.constraints.ReturnGuaranteesTypeError):
            fct(1)

    def test_false_with_conversion(self):
        @pg.constrain.returns(IsInt(force_conversion=True))
        def fct(a):
            return float(a)

        ret_val = fct(1)
        assert isinstance(ret_val, int)

    def test_multi(self):
        @pg.constrain.returns(IsInt(), IsInt())
        def fct(a, b):
            return a, b

        assert fct(1, 1) == (1, 1)

    def test_parameters_returns(self):
        @pg.constrain.parameters(a=IsInt())
        @pg.constrain.returns(IsStr())
        def fct(a):
            return str(a)

        assert fct(1) == str(1)

    def test_returns_paramters(self):
        @pg.constrain.returns(IsStr())
        @pg.constrain.parameters(a=IsInt())
        def fct(a):
            return str(a)

        assert fct(2) == str(2)
