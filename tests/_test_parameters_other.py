import unittest
from guarantees import functional_guarantees as fg


class TestIsClass(unittest.TestCase):
    def setUp(self) -> None:
        class TestClass:
            def __init__(self, a=1):
                self.a = a

        self.test_class = TestClass
        self.test_class_instance = TestClass()

    def test_base(self):
        @fg.add_guarantees(
            function_name="TestIsClass.test_base.fct",
            function_namespace="_test_parameters_other",
            param_guarantees=[
                fg.NoOp("a"),
                fg.IsClass("b", class_type=self.test_class)
            ]
        )
        def fct(a, b):
            return a, b

        # Check correct input
        fct("whatever", self.test_class_instance)
        fct(self.test_class_instance, self.test_class_instance)

        # Check errors
        try:
            fct(1, 1)
            self.assertTrue(False)  # should have raised exception
        except fg.exceptions.ParameterGuaranteesTypeError:
            self.assertTrue(True)  # successfully raised exception


class TestIsNone(unittest.TestCase):
    def test_type(self):
        @fg.add_guarantees(
            function_name="TestIsNone.test_type.fct",
            function_namespace="_test_parameters_other",
            param_guarantees=[
                fg.IsNone("a")
            ]
        )
        def fct(a):
            return a

        out = fct(None)
        self.assertIs(out, None)

        try:
            fct(1)
            self.assertTrue(False)  # should have raised exception
        except fg.exceptions.ParameterGuaranteesTypeError:
            self.assertTrue(True)  # successfully raised exception


class TestIsUnion(unittest.TestCase):
    def setUp(self) -> None:
        @fg.add_guarantees(
            function_name="TestIsUnion.setUp.fct",
            function_namespace="_test_parameters_other",
            param_guarantees=[
                fg.IsUnion(
                    "a",
                    guarantees=[
                        fg.IsInt("a"),
                        fg.IsNone("a"),
                        fg.IsStr("a")
                    ]
                )
            ]
        )
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
            self.assertTrue(False)  # should have raised exception
        except fg.exceptions.ParameterGuaranteesTypeError:
            self.assertTrue(True)  # successfully raised exception

    def test_value_error(self):
        @fg.add_guarantees(
            function_name="TestIsClass.test_value_error.fct",
            function_namespace="_test_parameters_other",
            param_guarantees=[
                fg.IsUnion(
                    "a",
                    guarantees=[
                        fg.IsInt("a", minimum=1),
                        fg.IsNone("a")
                    ]
                )
            ]
        )
        def fct(a):
            return a

        self.assertIs(fct(None), None)
        self.assertIsInstance(fct(1), int)

        try:
            fct(0)
            self.assertTrue(False)  # should have raised ValueError
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)  # successfully raised exception
