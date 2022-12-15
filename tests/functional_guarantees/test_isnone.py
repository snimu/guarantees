import pytest
from pyguarantees import functional_guarantees as fg


class TestIsNone:
    def test_is_none(self):
        @fg.add_guarantees(param_guarantees=[fg.IsNone("a")])
        def fct(a):
            return a

        out = fct(None)
        assert out is None

        with pytest.raises(fg.exceptions.ParameterGuaranteesTypeError):
            fct(1)
