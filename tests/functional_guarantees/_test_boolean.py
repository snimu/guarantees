import unittest

from guarantees import functional_guarantees as fg


class TestBooleanGuarantee(unittest.TestCase):
    def test_base(self):
        @fg.add_guarantees(param_guarantees=[fg.IsBool("a")])
        def fct(a):
            return a

        # Check if correct inputs work
        fct(True)
        fct(False)

        # Check if incorrect inputs raise exceptions
        try:
            fct("nope")
            self.assertTrue(False)   # should have raised an exception
        except fg.exceptions.ParameterGuaranteesTypeError:
            self.assertTrue(True)    # successfully raised exception

    def test_force_conversion(self):
        @fg.add_guarantees(
            param_guarantees=[fg.IsBool("a", force_conversion=True)]
        )
        def fct(a):
            return a

        # Basically everything in Python can be converted to bool; try a few
        #   to see if it works.
        b = fct(1)
        self.assertIs(type(b), bool)
        b = fct("hi")
        self.assertIs(type(b), bool)
        b = fct("")
        self.assertIs(type(b), bool)
        b = fct([])
        self.assertIs(type(b), bool)
        b = fct([1, 2, 3])
        self.assertIs(type(b), bool)
        b = fct(None)
        self.assertIs(type(b), bool)
