import unittest
import guarantees


class TestIsClass(unittest.TestCase):
    def setUp(self) -> None:
        class TestClass:
            def __init__(self, a=1):
                self.a = a
        self.test_class = TestClass
        self.test_class_instance = TestClass()

    def test_base(self):
        @guarantees.parameter_guarantees([
            guarantees.NoOp("a"),
            guarantees.IsClass("b", class_type=self.test_class)
        ])
        def fct(a, b):
            return a, b

        # Check correct input
        fct("whatever", self.test_class_instance)
        fct(self.test_class_instance, self.test_class_instance)

        # Check errors
        try:
            fct(1, 1)
            self.assertTrue(False)    # should have raised exception
        except TypeError:
            self.assertTrue(True)     # successfully raised exception

    def test_check_fct(self):
        def check_fct(arg):
            if arg.a != 1:
                raise ValueError("check_fct raised ValueError")

        @guarantees.parameter_guarantees([
            guarantees.IsClass("a", class_type=self.test_class,
                               check_fct=check_fct)
        ])
        def fct(a):
            return a

        # Check correct input
        fct(self.test_class_instance)

        # Check check_fct
        try:
            fct(self.test_class(2))
            self.assertTrue(False)   # should have raised exception
        except ValueError:
            self.assertTrue(True)    # successfully raised exception


class TestIsNone(unittest.TestCase):
    def test_type(self):
        @guarantees.parameter_guarantees([
            guarantees.IsNone("a")
        ])
        def fct(a):
            return a

        fct(None)

        try:
            fct(1)
            self.assertTrue(False)   # should have raised exception
        except TypeError:
            self.assertTrue(True)    # successfully raised exception
