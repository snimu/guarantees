import pytest

import pyguarantees as pg
from pyguarantees.constraints import IsInt


@pg.constrain.constrain(
    parameters=[
        IsInt("a"), IsInt("b"), IsInt("c")
    ]
)
def fct(a, b, c):
    return a, b, c


class TestParameterMatching:
    def test_correct_parameter_mixings(self):
        fct(1, 2, 3)
        fct(c=1, a=2, b=3)
        fct(1, c=3, b=1)

    def test_raise_exceptions_with_mixed_params(self):
        with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesTypeError):
            fct(1, b=2., c=3)