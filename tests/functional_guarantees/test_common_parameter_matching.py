import pytest

from pyguarantees import functional_guarantees as fg


@fg.add_guarantees(
    param_guarantees=[
        fg.IsInt("a"), fg.IsInt("b"), fg.IsInt("c")
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
        with pytest.raises(fg.exceptions.ParameterGuaranteesTypeError):
            fct(1, b=2., c=3)