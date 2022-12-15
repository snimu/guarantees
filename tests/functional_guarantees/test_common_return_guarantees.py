import pytest

from pyguarantees import functional_guarantees as fg


class TestReturnGuarantees:
    def test_correct(self) -> None:
        @fg.add_guarantees(return_guarantee=fg.IsInt("a"))
        def fct(a):
            return a

        ret_val = fct(1)
        assert isinstance(ret_val, int)

    def test_false(self):
        @fg.add_guarantees(return_guarantee=fg.IsInt("a"))
        def fct(a):
            return float(a)

        with pytest.raises(fg.exceptions.ReturnGuaranteesTypeError):
            fct(1)

    def test_false_with_conversion(self):
        @fg.add_guarantees(return_guarantee=fg.IsInt("a", force_conversion=True))
        def fct(a):
            return float(a)

        ret_val = fct(1)
        assert isinstance(ret_val, int)
