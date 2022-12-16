import pytest
from pyguarantees import functional_guarantees as fg


@fg.add_guarantees(param_guarantees=[
    fg.IsInt("a"),
    fg.IsFloat("b"),
    fg.IsComplex("c")
])
def fct_base(a, b, c):
    return a, b, c


class TestNumericBase:
    def test_correct(self):
        fct_base(1, 1.0, complex(1., 1.))

    def test_violations(self):
        false_input_int = [1., 1., complex(1., 1.)]
        false_input_flot = [1, 1, complex(1., 1.)]
        false_input_complex = [1, 1., 1]

        for inputs in [false_input_int, false_input_flot, false_input_complex]:
            with pytest.raises(fg.exceptions.ParameterGuaranteesTypeError):
                fct_base(*inputs)


@fg.add_guarantees(param_guarantees=[
    fg.IsInt("a", force_conversion=True),
    fg.IsFloat("b", force_conversion=True),
    fg.IsComplex("c", force_conversion=True)
])
def fct_force_conversion(a, b, c):
    return a, b, c


class TestNumericForceConversion:
    def test_correct(self):

        # Test conversion
        a, b, c = fct_force_conversion(1., 1, 1.)
        assert type(a) is int, "Should be int."
        assert type(b) is float, "Should be float."
        assert type(c) is complex, "Should be complex."

        a, b, c = fct_force_conversion("1", "1", "1")
        assert type(a) is int, "Should be int."
        assert type(b) is float, "Should be float."
        assert type(c) is complex, "Should be complex."

    def test_violations(self):
        false_inputs_int = ["nope", 1., complex(1., 1.)]
        false_inputs_float = [1, "nope", complex(1., 1.)]
        false_inputs_complex = [1, 1., "nope"]

        for inputs in [false_inputs_int, false_inputs_float, false_inputs_complex]:
            with pytest.raises(fg.exceptions.ParameterGuaranteesTypeError):
                fct_force_conversion(*inputs)


@fg.add_guarantees(param_guarantees=[
    fg.IsInt("a", minimum=0, maximum=5),
    fg.IsFloat("b", minimum=0., maximum=5.),
    fg.IsComplex("c", minimum=1., maximum=5., minimum_re=0.,
                 maximum_re=5., minimum_im=0., maximum_im=5.)
])
def fct_minmax(a, b, c):
    return a, b, c


class TestNumericMinMax:
    def test_correct(self):
        fct_minmax(0, 0., complex(1., 1.))
        fct_minmax(5, 5., complex(5., 0.))   # must not be too big in absolute value!
        fct_minmax(5, 5., complex(0., 5.))
        fct_minmax(2, 3., complex(2., 2.))   # something in-between

    def test_violations(self):
        false_inputs = [
            [-1, 0., complex(1., 1.)],   # a too small
            [6, 0., complex(1., 1.)],   # a too large
            [0, -1., complex(1., 1.)],   # b too small
            [0, 6., complex(1., 1.)],   # b too large
            [0, 0., complex(0., 0.)],   # c.abs too small
            [0, 0., complex(5., 5.)],   # c.abs too large
            [0, 0., complex(-1., 0.)],   # c.re too small
            [0, 0., complex(6., 0.)],   # c.re too large
            [0, 0., complex(0., -1.)],   # c.im too small
            [0, 0., complex(0., 6.)]   # c.im too large
        ]

        for inputs in false_inputs:
            with pytest.raises(fg.exceptions.ParameterGuaranteesValueError):
                fct_minmax(*inputs)


@fg.add_guarantees(param_guarantees=[
    fg.IsInt("a", isin=[1, 2]),
    fg.IsFloat("b", isin=[1., 2.]),
    fg.IsComplex("c", isin=[complex(0., 0.), complex(1., 1.)])
])
def fct_isin(a, b, c):
    return a, b, c


class TestNumericIsIn:
    def test_correct(self):
        fct_isin(1, 1., complex(0., 0.))
        fct_isin(1, 2., complex(0., 0.))
        fct_isin(2, 1., complex(0., 0.))
        fct_isin(2, 2., complex(0., 0.))
        fct_isin(1, 1., complex(1., 1.))
        fct_isin(1, 2., complex(1., 1.))
        fct_isin(2, 1., complex(1., 1.))
        fct_isin(2, 2., complex(1., 1.))

    def test_violations(self):
        false_inputs = [
            [4, 0., complex(0., 0.)],
            [0, 4., complex(0., 0.)],
            [0, 0., complex(4., 0.)],
            [0, 0., complex(0., 4.)]
        ]

        for inputs in false_inputs:
            with pytest.raises(fg.exceptions.ParameterGuaranteesValueError):
                fct_isin(*inputs)


class TestNumericIncorrectGuaranteeInputs:
    def test_min_int(self):
        @fg.add_guarantees(param_guarantees=[fg.IsInt("a", minimum="nope")])
        def fct(a):
            return a

        with pytest.raises(fg.exceptions.FunctionalGuaranteesUserTypeError):
            fct(1)

    def test_min_float(self):
        @fg.add_guarantees(param_guarantees=[fg.IsFloat("a", minimum="nope")])
        def fct(a):
            return a

        with pytest.raises(fg.exceptions.FunctionalGuaranteesUserTypeError):
            fct(1.)

    def test_min_complex(self):
        @fg.add_guarantees(param_guarantees=[fg.IsComplex("a", minimum="nope")])
        def fct(a):
            return a

        with pytest.raises(fg.exceptions.FunctionalGuaranteesUserTypeError):
            fct(complex(1., 1.))

    def test_min_re_complex(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsComplex("a", minimum_re="nope")
        ])
        def fct(a):
            return a

        with pytest.raises(fg.exceptions.FunctionalGuaranteesUserTypeError):
            fct(complex(1., 1.))

    def test_min_im_complex(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsComplex("a", minimum_im="nope")
        ])
        def fct(a):
            return a

        with pytest.raises(fg.exceptions.FunctionalGuaranteesUserTypeError):
            fct(complex(1., 1.))

    def test_max_int(self):
        @fg.add_guarantees(param_guarantees=[fg.IsInt("a", maximum="nope")])
        def fct(a):
            return a

        with pytest.raises(fg.exceptions.FunctionalGuaranteesUserTypeError):
            fct(1)

    def test_max_float(self):
        @fg.add_guarantees(param_guarantees=[fg.IsFloat("a", maximum="nope")])
        def fct(a):
            return a

        with pytest.raises(fg.exceptions.FunctionalGuaranteesUserTypeError):
            fct(1.)

    def test_max_complex(self):
        @fg.add_guarantees(param_guarantees=[fg.IsComplex("a", maximum="nope")])
        def fct(a):
            return a

        with pytest.raises(fg.exceptions.FunctionalGuaranteesUserTypeError):
            fct(complex(1., 1.))

    def test_max_complex_re(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsComplex("a", maximum_re="nope")
        ])
        def fct(a):
            return a

        with pytest.raises(fg.exceptions.FunctionalGuaranteesUserTypeError):
            fct(complex(1., 1.))

    def test_max_complex_im(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsComplex("a", maximum_im="nope")
        ])
        def fct(a):
            return a

        with pytest.raises(fg.exceptions.FunctionalGuaranteesUserTypeError):
            fct(complex(1., 1.))

    def test_isin_int(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsInt("a", isin="nope")
        ])
        def fct(a):
            return a

        with pytest.raises(fg.exceptions.FunctionalGuaranteesUserTypeError):
            fct(1)

    def test_isin_float(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsFloat("a", isin="nope")
        ])
        def fct(a):
            return a

        with pytest.raises(fg.exceptions.FunctionalGuaranteesUserTypeError):
            fct(1.)

    def test_isin_complex(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsComplex("a", isin="nope")
        ])
        def fct(a):
            return a

        with pytest.raises(fg.exceptions.FunctionalGuaranteesUserTypeError):
            fct(complex(1., 1.))