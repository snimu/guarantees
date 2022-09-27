import unittest
from guarantees import functional_guarantees as fg


class TestNumericGuarantee(unittest.TestCase):
    def test_basic(self):
        @fg.parameter_guarantees([
            fg.IsInt("a"),
            fg.IsFloat("b"),
            fg.IsComplex("c")
        ])
        def fct(a, b, c):
            return a, b, c

        # Correct types -> no error should be raised
        fct(1, 1.0, complex(1., 1.))

        # Float for int, int for float, float for complex -> should raise
        #   error even though it is convertible
        try:
            fct(1., 1., complex(1., 1.))
            self.assertTrue(False)   # should have raised an error
        except TypeError:
            self.assertTrue(True)    # successfully raised exception

        try:
            fct(1, 1, complex(1., 1.))
            self.assertTrue(False)   # param b should have raised error
        except TypeError:
            self.assertTrue(True)    # successfully raised exception

        try:
            fct(1, 1., 1.)
            self.assertTrue(False)   # param c should have raised error
        except TypeError:
            self.assertTrue(True)    # successfully raised exception

    def test_force_conversion(self):
        @fg.parameter_guarantees([
            fg.IsInt("a", force_conversion=True),
            fg.IsFloat("b", force_conversion=True),
            fg.IsComplex("c", force_conversion=True)
        ])
        def fct(a, b, c):
            return a, b, c

        # Test conversion
        a, b, c = fct(1., 1, 1.)
        self.assertIs(type(a), int, "Should be int.")
        self.assertIs(type(b), float, "Should be float.")
        self.assertIs(type(c), complex, "Should be complex.")

        a, b, c = fct("1", "1", "1")
        self.assertIs(type(a), int, "Should be int.")
        self.assertIs(type(b), float, "Should be float.")
        self.assertIs(type(c), complex, "Should be complex.")

        # Test conversion fail
        try:
            fct("nope", 1., complex(1., 1.))
            self.assertTrue(False)    # param a should have raise error
        except TypeError:
            self.assertTrue(True)     # successfully raised exception

        try:
            fct(1, "nope", complex(1., 1.))
            self.assertTrue(False)  # param b should have raise error
        except TypeError:
            self.assertTrue(True)  # successfully raised exception

        try:
            fct(1, 1., "nope")
            self.assertTrue(False)    # param c should have raise error
        except TypeError:
            self.assertTrue(True)     # successfully raised exception

    def test_minmax(self):
        @fg.parameter_guarantees([
            fg.IsInt("a", minimum=0, maximum=5),
            fg.IsFloat("b", minimum=0., maximum=5.),
            fg.IsComplex("c", minimum=0., maximum=5., minimum_re=0.,
                         maximum_re=5., minimum_im=0., maximum_im=5.)
        ])
        def fct(a, b, c):
            return a, b, c

        # Check correct inputs
        fct(0, 0., complex(0., 0.))
        fct(5, 5., complex(5., 0.))   # must not be too big in absolute value!
        fct(5, 5., complex(0., 5.))
        fct(2, 3., complex(1., 1.))   # something in-between

        # Check that errors are raised
        try:
            fct(-1, 0., complex(0., 0.))    # param a too small
            self.assertTrue(False)    # should raise an exception
        except ValueError:
            self.assertTrue(True)     # successfully raised exception

        try:
            fct(6, 0., complex(0., 0.))     # param a too large
            self.assertTrue(False)    # should raise an exception
        except ValueError:
            self.assertTrue(True)     # successfully raised exception

        try:
            fct(0, -1., complex(0., 0.))     # param b too small
            self.assertTrue(False)    # should raise an exception
        except ValueError:
            self.assertTrue(True)     # successfully raised exception

        try:
            fct(0, 6., complex(0., 0.))     # param b too large
            self.assertTrue(False)    # should raise an exception
        except ValueError:
            self.assertTrue(True)     # successfully raised exception

        try:
            fct(0, 0., complex(5., 5.))    # abs value of param c too great
            self.assertTrue(False)    # should raise an exception
        except ValueError:
            self.assertTrue(True)     # successfully raised exception

        try:
            fct(0, 0., complex(-1., 0.))    # param c.real too small
            self.assertTrue(False)    # should raise an exception
        except ValueError:
            self.assertTrue(True)     # successfully raised exception

        try:
            fct(0, 0., complex(6., 0.))     # param c.real too large
            self.assertTrue(False)    # should raise an exception
        except ValueError:
            self.assertTrue(True)     # successfully raised exception

        try:
            fct(0, 0., complex(0., -1.))    # param c.imag too small
            self.assertTrue(False)    # should raise an exception
        except ValueError:
            self.assertTrue(True)     # successfully raised exception

        try:
            fct(0, 0., complex(0., 6.))     # param c.imag too large
            self.assertTrue(False)    # should raise an exception
        except ValueError:
            self.assertTrue(True)     # successfully raised exception

    def test_isin(self):
        @fg.parameter_guarantees([
            fg.IsInt("a", isin=[1, 2]),
            fg.IsFloat("b", isin=[1., 2.]),
            fg.IsComplex("c", isin=[complex(0., 0.), complex(1., 1.)])
        ])
        def fct(a, b, c):
            return a, b, c

        # Check correct running
        fct(1, 1., complex(0., 0.))
        fct(1, 2., complex(0., 0.))
        fct(2, 1., complex(0., 0.))
        fct(2, 2., complex(0., 0.))
        fct(1, 1., complex(1., 1.))
        fct(1, 2., complex(1., 1.))
        fct(2, 1., complex(1., 1.))
        fct(2, 2., complex(1., 1.))

        # Check correct error raising
        try:
            fct(4, 0., complex(0., 0.))
            self.assertTrue(False)   # param a should have raised exception
        except ValueError:
            self.assertTrue(True)    # successfully raised exception

        try:
            fct(0, 4., complex(0., 0.))
            self.assertTrue(False)   # param a should have raised exception
        except ValueError:
            self.assertTrue(True)    # successfully raised exception

        try:
            fct(0, 0., complex(4., 0.))
            self.assertTrue(False)   # param a should have raised exception
        except ValueError:
            self.assertTrue(True)    # successfully raised exception

        try:
            fct(0, 0., complex(0., 4.))
            self.assertTrue(False)   # param a should have raised exception
        except ValueError:
            self.assertTrue(True)    # successfully raised exception

    def test_incorrect_guarantee_parameters_int_min(self):
        @fg.parameter_guarantees([
            fg.IsInt("a", minimum="nope")
        ])
        def fct(a):
            return a

        try:
            fct(1)
            self.assertTrue(False)   # should have raised exception
        except TypeError:
            self.assertTrue(True)    # successfully raised exception

    def test_incorrect_guarantee_parameters_float_min(self):
        @fg.parameter_guarantees([
            fg.IsFloat("a", minimum="nope")
        ])
        def fct(a):
            return a

        try:
            fct(1.)
            self.assertTrue(False)  # should have raised exception
        except TypeError:
            self.assertTrue(True)  # successfully raised exception

    def test_incorrect_guarantee_parameters_complex_min(self):
        @fg.parameter_guarantees([
            fg.IsComplex("a", minimum="nope")
        ])
        def fct(a):
            return a

        try:
            fct(complex(1., 1.))
            self.assertTrue(False)  # should have raised exception
        except TypeError:
            self.assertTrue(True)  # successfully raised exception

    def test_incorrect_guarantee_parameters_complex_min_re(self):
        @fg.parameter_guarantees([
            fg.IsComplex("a", minimum_re="nope")
        ])
        def fct(a):
            return a

        try:
            fct(complex(1., 1.))
            self.assertTrue(False)  # should have raised exception
        except TypeError:
            self.assertTrue(True)  # successfully raised exception

    def test_incorrect_guarantee_parameters_complex_min_im(self):
        @fg.parameter_guarantees([
            fg.IsComplex("a", minimum_im="nope")
        ])
        def fct(a):
            return a

        try:
            fct(complex(1., 1.))
            self.assertTrue(False)  # should have raised exception
        except TypeError:
            self.assertTrue(True)  # successfully raised exception

    def test_incorrect_guarantee_parameters_int_max(self):
        @fg.parameter_guarantees([
            fg.IsInt("a", maximum="nope")
        ])
        def fct(a):
            return a

        try:
            fct(1)
            self.assertTrue(False)  # should have raised exception
        except TypeError:
            self.assertTrue(True)  # successfully raised exception

    def test_incorrect_guarantee_parameters_float_max(self):
        @fg.parameter_guarantees([
            fg.IsFloat("a", maximum="nope")
        ])
        def fct(a):
            return a

        try:
            fct(1.)
            self.assertTrue(False)  # should have raised exception
        except TypeError:
            self.assertTrue(True)  # successfully raised exception

    def test_incorrect_guarantee_parameters_complex_max(self):
        @fg.parameter_guarantees([
            fg.IsComplex("a", maximum="nope")
        ])
        def fct(a):
            return a

        try:
            fct(complex(1., 1.))
            self.assertTrue(False)  # should have raised exception
        except TypeError:
            self.assertTrue(True)  # successfully raised exception

    def test_incorrect_guarantee_parameters_complex_max_re(self):
        @fg.parameter_guarantees([
            fg.IsComplex("a", maximum_re="nope")
        ])
        def fct(a):
            return a

        try:
            fct(complex(1., 1.))
            self.assertTrue(False)  # should have raised exception
        except TypeError:
            self.assertTrue(True)  # successfully raised exception

    def test_incorrect_guarantee_parameters_complex_max_im(self):
        @fg.parameter_guarantees([
            fg.IsComplex("a", maximum_im="nope")
        ])
        def fct(a):
            return a

        try:
            fct(complex(1., 1.))
            self.assertTrue(False)  # should have raised exception
        except TypeError:
            self.assertTrue(True)  # successfully raised exception

    def test_incorrect_guarantee_parameters_int_isin(self):
        @fg.parameter_guarantees([
            fg.IsInt("a", isin="nope")
        ])
        def fct(a):
            return a

        try:
            fct(1)
            self.assertTrue(False)  # should have raised exception
        except TypeError:
            self.assertTrue(True)  # successfully raised exception

    def test_incorrect_guarantee_parameters_float_isin(self):
        @fg.parameter_guarantees([
            fg.IsFloat("a", isin="nope")
        ])
        def fct(a):
            return a

        try:
            fct(1.)
            self.assertTrue(False)  # should have raised exception
        except TypeError:
            self.assertTrue(True)  # successfully raised exception

    def test_incorrect_guarantee_parameters_complex_isin(self):
        @fg.parameter_guarantees([
            fg.IsComplex("a", isin="nope")
        ])
        def fct(a):
            return a

        try:
            fct(complex(1., 1.))
            self.assertTrue(False)  # should have raised exception
        except TypeError:
            self.assertTrue(True)  # successfully raised exception


# TODO: test_mixed_arg_kwarg in _test_parameters_guarantee_base
