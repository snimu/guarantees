import pytest
import pyguarantees as pg
from pyguarantees.constraints import (
    NoOp,
    IsClass
)


class ExampleClass:
    def __init__(self, a=1):
        self.a = a


example_class = ExampleClass()


@pg.constrain.parameters(
    a=NoOp(),
    b=IsClass(class_type=ExampleClass)
)
def fct(a, b):
    return a, b


class TestIsClass:
    def test_correct(self):
        fct("whatever", example_class)
        fct(example_class, example_class)

    def test_violations(self):
        with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesTypeError):
            fct(1, 1)
