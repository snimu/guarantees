import pytest
import pyguarantees as pg
from pyguarantees.constraints import (
    IsUnion,
    IsInt,
    IsNone,
    IsStr
)


@pg.constrain.parameters(
    a=IsUnion(
        guarantees=[
            IsInt("a"),
            IsNone("a"),
            IsStr("a")
        ]
    )
)
def fct(a):
    return a


class TestIsUnion:
    def test_correct_inputs(self):
        out = fct(None)
        assert out is None
        out = fct(1)
        assert isinstance(out, int)
        out = fct("hi :)")
        assert isinstance(out, str)

    def test_wrong_inputs(self):
        with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesTypeError):
            fct(complex(1., 1.))

    def test_value_error(self):
        @pg.constrain.parameters(
            a=IsUnion(
                guarantees=[
                    IsInt(minimum=1),
                    IsNone()
                ]
            )
        )
        def fct_value_error(a):
            return a

        assert fct_value_error(None) is None
        assert isinstance(fct_value_error(1), int)

        with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesValueError):
            fct_value_error(0)
