import pytest
from pyguarantees import functional_guarantees as fg


class ExampleClass:
    def __init__(self, a=1):
        self.a = a


example_class = ExampleClass()


@fg.add_guarantees(param_guarantees=[
    fg.NoOp("a"),
    fg.IsClass("b", class_type=ExampleClass)
])
def fct(a, b):
    return a, b


class TestIsClass:
    def test_correct(self):
        fct("whatever", example_class)
        fct(example_class, example_class)

    def test_violations(self):
        with pytest.raises(fg.exceptions.ParameterGuaranteesTypeError):
            fct(1, 1)
