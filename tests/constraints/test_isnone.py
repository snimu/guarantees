import pytest
import pyguarantees as pg
from pyguarantees.constraints import IsNone


class TestIsNone:
    def test_is_none(self):
        @pg.constrain.parameters(a=IsNone())
        def fct(a):
            return a

        out = fct(None)
        assert out is None

        with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesTypeError):
            fct(1)
