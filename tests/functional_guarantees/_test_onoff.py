import unittest
from pyguarantees import functional_guarantees as fg


class TestOnOff(unittest.TestCase):
    def test_onoff(self):
        @fg.add_guarantees(param_guarantees=[fg.IsInt("a")])
        def fct(a):
            return a

        # Check that it works in general
        val = fct(1)
        self.assertIsInstance(val, int)

        self.assertRaises(
            fg.exceptions.ParameterGuaranteesTypeError,
            fct, "not an int!"
        )

        fg.decorator.settings.change_settings(active=False)
        fct("not an int!")

        fg.decorator.settings.change_settings(active=True)
        self.assertRaises(
            fg.exceptions.ParameterGuaranteesTypeError,
            fct, "not an int!"
        )


def test_onoff():
    """TestOnOff cannot be run as part of unittest.main(), because all tests
    are run in parallel and pyguarantees.off() would impact all other tests.
    Therefore, provide this function to be run before or after running
    unittest.main()."""
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestOnOff)
    a = unittest.TextTestRunner().run(suite)
    return a
