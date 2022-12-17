import pytest

import pyguarantees as pg
from pyguarantees.constraints import (
    IsInt,
    DynamicCheck
)


@pg.constrain.constrain(parameters=[
    IsInt(
        "a",
        dynamic_checks=[
            DynamicCheck(check=lambda x: x % 3 == 0),
            DynamicCheck(check=lambda x: x ** 2 - 2 * x < 1e4)
        ])
])
def fct(a):
    return a


@pg.constrain.constrain(parameters=[
    IsInt(
        "a",
        dynamic_checks=[
            DynamicCheck(
                description="divisible by 3",
                check=lambda x: x % 3 == 0
            ),
            DynamicCheck(
                description="on correct side of decision boundary",
                check=lambda x: x**2 - 2 * x < 1e4
            )
        ])
])
def fct_description(a):
    return a


@pg.constrain.constrain(parameters=[
    IsInt(
        "a",
        dynamic_checks=[
            DynamicCheck(
                description="divisible by 3",
                check=lambda x: x % 3 == 0,
                callback=lambda x: print(x)
            ),
            DynamicCheck(
                description="on correct side of decision boundary",
                check=lambda x: x ** 2 - 2 * x < 1e4,
                callback=lambda x: print(x)
            )
        ])
])
def fct_description_callback(a):
    return a


functions = [fct, fct_description, fct_description_callback]


class TestDynamicChecks:
    def test_correct(self):
        for f in functions:
            f(3)
            f(6)
            f(9)

    def test_check1_err(self):
        for f in functions:
            with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesValueError):
                f(2)

    def test_check2_err(self):
        for f in functions:
            with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesValueError):
                f(3**10)
