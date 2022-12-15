import unittest
from pyguarantees import functional_guarantees as fg


class TestIsClass(unittest.TestCase):
    def setUp(self) -> None:
        class TestClass:
            def __init__(self, a=1):
                self.a = a

        @fg.add_guarantees(param_guarantees=[
            fg.NoOp("a"),
            fg.IsClass("b", class_type=self.test_class)
        ])
        def fct(a, b):
            return a, b

        self.test_class = TestClass
        self.test_class_instance = TestClass()
        self.fct = fct

    def test_correct(self):
        self.fct("whatever", self.test_class_instance)
        self.fct(self.test_class_instance, self.test_class_instance)

    def test_violations(self):
        self.assertRaises(
            fg.exceptions.ParameterGuaranteesTypeError,
            self.fct, 1, 1
        )


class TestIsNone(unittest.TestCase):
    def test_is_none(self):
        @fg.add_guarantees(param_guarantees=[fg.IsNone("a")])
        def fct(a):
            return a

        out = fct(None)
        self.assertIs(out, None)
        self.assertRaises(fg.exceptions.ParameterGuaranteesTypeError, fct, 1)


class TestIsUnion(unittest.TestCase):
    def setUp(self) -> None:
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

        self.fct = fct

    def test_correct_inputs(self):
        out = self.fct(None)
        self.assertIs(out, None)
        out = self.fct(1)
        self.assertIsInstance(out, int)
        out = self.fct("hi :)")
        self.assertIsInstance(out, str)

    def test_wrong_inputs(self):
        self.assertRaises(
            fg.exceptions.ParameterGuaranteesTypeError,
            self.fct, complex(1., 1.)
        )

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
        def fct(a):
            return a

        self.assertIs(fct(None), None)
        self.assertIsInstance(fct(1), int)
        self.assertRaises(fg.exceptions.ParameterGuaranteesValueError, fct, 0)
