import pytest

from pyguarantees import functional_guarantees as fg


class TestBooleanGuarantee:
    def test_base(self):
        @fg.add_guarantees(param_guarantees=[fg.IsBool("a")])
        def fct(a):
            return a

        # Check if correct inputs work
        fct(True)
        fct(False)

        # Check if incorrect inputs raise exceptions
        with pytest.raises(fg.exceptions.ParameterGuaranteesTypeError):
            fct("nope")

    def test_force_conversion(self):
        @fg.add_guarantees(
            param_guarantees=[fg.IsBool("a", force_conversion=True)]
        )
        def fct(a):
            return a

        # Basically everything in Python can be converted to bool; try a few
        #   to see if it works.
        b = fct(1)
        assert type(b) is bool
        b = fct("hi")
        assert type(b) is bool
        b = fct("")
        assert type(b) is bool
        b = fct([])
        assert type(b) is bool
        b = fct([1, 2, 3])
        assert type(b) is bool
        b = fct(None)
        assert type(b) is bool
