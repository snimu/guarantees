import pytest

import pyguarantees as pg
from pyguarantees.constraints import (
    IsInt,
    IsBytes
)


@pg.constrain.constrain(
    parameters=[
        IsInt("a", forbidden_values=[1, 2, 3]),
        IsBytes("b", forbidden_values=[b"123", b"111"])
    ]
)
def fct(a, b):
    return a, b


class TestForbiddenValues:
    def test_legal_values(self):
        fct(0, b"000")
        fct(5, b"321")
        fct(-10, b"001")

    def test_forbidden_values(self):
        for inputs in [[1, b"000"], [0, b"123"]]:
            with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesValueError):
                fct(*inputs)
