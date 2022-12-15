import pytest
from pyguarantees import functional_guarantees as fg


@fg.add_guarantees(param_guarantees=[
    fg.IsUnion(
        "a",
        guarantees=[
            fg.IsInt("a"),
            fg.IsNone("a"),
            fg.IsStr("a")
        ]
    )
])
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

    def test_wrong_inputs(self):
        with pytest.raises(fg.exceptions.ParameterGuaranteesTypeError):
            fct(complex(1., 1.))

    def test_value_error(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsUnion(
                "a",
                guarantees=[
                    fg.IsInt("a", minimum=1),
                    fg.IsNone("a")
                ]
            )
        ])
        def fct_value_error(a):
            return a

        assert fct_value_error(None) is None
        assert isinstance(fct_value_error(1), int)

        with pytest.raises(fg.exceptions.ParameterGuaranteesValueError):
            fct_value_error(0)
