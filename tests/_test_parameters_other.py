import unittest
from guarantees import parameter_guarantees as pg


class TestIsClass(unittest.TestCase):
    def setUp(self) -> None:
        class TestClass:
            def __init__(self, a=1):
                self.a = a
        self.test_class = TestClass
        self.test_class_instance = TestClass()

    def test_base(self):
        @pg.parameter_guarantees([
            pg.NoOp("a"),
            pg.IsClass("b", class_type=self.test_class)
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

        @pg.parameter_guarantees([
            pg.IsClass("a", class_type=self.test_class,
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
        @pg.parameter_guarantees([
            pg.IsNone("a")
        ])
        def fct(a):
            return a

        out = fct(None)
        self.assertIs(out, None)

        try:
            fct(1)
            self.assertTrue(False)   # should have raised exception
        except TypeError:
            self.assertTrue(True)    # successfully raised exception


class TestIsUnion(unittest.TestCase):
    def setUp(self) -> None:
        @pg.parameter_guarantees([
            pg.IsUnion(
                "a",
                guarantees=[
                    pg.IsInt("a"),
                    pg.IsNone("a"),
                    pg.IsStr("a")
                ]
            )
        ])
        def fct(a):
            return a

        self.fct = fct

    def test_correct_inputs(self):
        out = self.fct(None)
        self.assertIs(out, None)
        out = self.fct(1)
        self.assertIsInstance(out, int)
        out = self.fct("hi :)")
        self.assertIsInstance(out, str)

    def test_wrong_inputs(self):
        try:
            self.fct(complex(1., 1.))
            self.assertTrue(False)   # should have raised exception
        except TypeError:
            self.assertTrue(True)    # successfully raised exception

    def test_value_error(self):
        @pg.parameter_guarantees([
            pg.IsUnion(
                "a",
                guarantees=[
                    pg.IsInt("a", minimum=1),
                    pg.IsNone("a")
                ]
            )
        ])
        def fct(a):
            return a

        self.assertIs(fct(None), None)
        self.assertIsInstance(fct(1), int)

        try:
            fct(0)
            self.assertTrue(False)   # should have raised ValueError
        except ValueError:
            self.assertTrue(True)    # successfully raised exception
