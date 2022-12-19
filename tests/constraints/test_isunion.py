import pytest
import pyguarantees as pg
from pyguarantees.constraints import (
    IsUnion,
    IsInt,
    IsNone,
    IsStr,
    IsClass,
    NoOp,
    DynamicCheck
)


class ExampleClass:
    pass


@pg.constrain.parameters(
    a=IsUnion(
        guarantees=[
            IsInt(),
            IsNone(),
            IsStr(),
            IsClass(class_type=ExampleClass)
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
        out = fct(ExampleClass())
        assert isinstance(out, ExampleClass)

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

    def test_dynamic_checks(self):
        @pg.constrain.parameters(
            a=IsUnion(
                guarantees=[
                    IsInt(
                        dynamic_checks=[
                            DynamicCheck(check=lambda x: x % 3 == 0, description="divisible by 3")
                        ]
                    )
                ]
            )
        )
        def fct(a):
            return a

        assert fct(3) == 3

        with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesValueError):
            fct(1)

    def test_forbidden_values(self):
        @pg.constrain.parameters(a=IsUnion(guarantees=[IsInt(forbidden_values=[0])]))
        def fct(a):
            return a

        assert fct(1) == 1

        with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesValueError):
            fct(0)

    def test_recursive(self):
        @pg.constrain.parameters(
            a=IsUnion(
                guarantees=[
                    IsUnion(
                        guarantees=[
                            IsInt()
                        ]
                    )
                ]
            )
        )
        def fct(a):
            return a

        with pytest.raises(pg.exceptions.constraints.FunctionalGuaranteesUserTypeError):
            fct(1)

    def test_noop(self):
        @pg.constrain.parameters(a=IsUnion(guarantees=[NoOp()]))
        def fct(a):
            return a

        with pytest.raises(pg.exceptions.constraints.FunctionalGuaranteesUserTypeError):
            fct(1)
