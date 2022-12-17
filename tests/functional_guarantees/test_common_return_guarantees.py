import pytest

import pyguarantees as pg
from pyguarantees.constraints import IsInt


class TestReturnGuarantees:
    def test_correct(self) -> None:
        @pg.constrain.constrain(returns=IsInt("a"))
        def fct(a):
            return a

        ret_val = fct(1)
        assert isinstance(ret_val, int)

    def test_false(self):
        @pg.constrain.constrain(returns=IsInt("a"))
        def fct(a):
            return float(a)

        with pytest.raises(pg.exceptions.constraints.ReturnGuaranteesTypeError):
            fct(1)

    def test_false_with_conversion(self):
        @pg.constrain.constrain(returns=IsInt("a", force_conversion=True))
        def fct(a):
            return float(a)

        ret_val = fct(1)
        assert isinstance(ret_val, int)
