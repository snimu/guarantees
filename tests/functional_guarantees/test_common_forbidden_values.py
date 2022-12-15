import pytest

from pyguarantees import functional_guarantees as fg


@fg.add_guarantees(
    param_guarantees=[
        fg.IsInt("a", forbidden_values=[1, 2, 3]),
        fg.IsBytes("b", forbidden_values=[b"123", b"111"])
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
            with pytest.raises(fg.exceptions.ParameterGuaranteesValueError):
                fct(*inputs)
