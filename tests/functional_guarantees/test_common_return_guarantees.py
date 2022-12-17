import pytest

import pyguarantees as pg
from pyguarantees.constraints import IsInt


class TestReturnGuarantees:
    def test_correct(self) -> None:
        @pg.constrain.returns(IsInt())
        def fct(a):
            return a

        ret_val = fct(1)
        import warnings
        warnings.warn(str(ret_val))
        assert isinstance(ret_val, int)

    @pytest.mark.skip
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
