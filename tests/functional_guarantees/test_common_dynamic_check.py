import pytest

from pyguarantees import functional_guarantees as fg


@fg.add_guarantees(param_guarantees=[
    fg.IsInt(
        "a",
        dynamic_checks=[
            fg.DynamicCheck(check=lambda x: x % 3 == 0),
            fg.DynamicCheck(check=lambda x: x ** 2 - 2 * x < 1e4)
        ])
])
def fct(a):
    return a


@fg.add_guarantees(param_guarantees=[
    fg.IsInt(
        "a",
        dynamic_checks=[
            fg.DynamicCheck(
                description="divisible by 3",
                check=lambda x: x % 3 == 0
            ),
            fg.DynamicCheck(
                description="on correct side of decision boundary",
                check=lambda x: x**2 - 2 * x < 1e4
            )
        ])
])
def fct_description(a):
    return a


@fg.add_guarantees(param_guarantees=[
    fg.IsInt(
        "a",
        dynamic_checks=[
            fg.DynamicCheck(
                description="divisible by 3",
                check=lambda x: x % 3 == 0,
                callback=lambda x: print(x)
            ),
            fg.DynamicCheck(
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
            with pytest.raises(fg.exceptions.ParameterGuaranteesValueError):
                f(2)

    def test_check2_err(self):
        for f in functions:
            with pytest.raises(fg.exceptions.ParameterGuaranteesValueError):
                f(3**10)
