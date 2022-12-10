import unittest
from pyguarantees import functional_guarantees as fg


class CbException(Exception):
    pass


class TestCallback(unittest.TestCase):
    def setUp(self) -> None:
        def cb(signal):
            raise CbException("success")

        self.cb = cb

    def test_isint_cb(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsInt("a", error_callback=self.cb)
        ])
        def fct(a):
            return a

        try:
            fct(1.)
            self.assertTrue(False)  # should have raised an exception
        except CbException:
            self.assertTrue(True)  # successfully raised exception

    def test_isstr_cb(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsStr("a", error_callback=self.cb)
        ])
        def fct(a):
            return a

        try:
            fct(1.)
            self.assertTrue(False)  # should have raised an exception
        except CbException:
            self.assertTrue(True)  # successfully raised exception

    def test_islist_cb(self):
        @fg.add_guarantees(param_guarantees=[
            fg.IsList("a", error_callback=self.cb)
        ])
        def fct(a):
            return a

        try:
            fct(1.)
            self.assertTrue(False)  # should have raised an exception
        except CbException:
            self.assertTrue(True)  # successfully raised exception


class TestCheckFunctions(unittest.TestCase):
    def setUp(self) -> None:
        @fg.add_guarantees(param_guarantees=[
            fg.IsInt(
                "a",
                dynamic_checks=[
                    fg.DynamicCheck(check=lambda x: x % 3 == 0),
                    fg.DynamicCheck(check=lambda x: x ** 2 - 2 * x < 1e4)
                ])
        ])
        def fct(a):
            return a

        @fg.add_guarantees(param_guarantees=[
            fg.IsInt(
                "a",
                dynamic_checks=[
                    fg.DynamicCheck(
                        description="divisible by 3",
                        check=lambda x: x % 3 == 0
                    ),
                    fg.DynamicCheck(
                        description="on correct side of decision boundary",
                        check=lambda x: x**2 - 2 * x < 1e4
                    )
                ])
        ])
        def fct_description(a):
            return a

        @fg.add_guarantees(param_guarantees=[
            fg.IsInt(
                "a",
                dynamic_checks=[
                    fg.DynamicCheck(
                        description="divisible by 3",
                        check=lambda x: x % 3 == 0,
                        callback=lambda x: print(x)
                    ),
                    fg.DynamicCheck(
                        description="on correct side of decision boundary",
                        check=lambda x: x ** 2 - 2 * x < 1e4,
                        callback=lambda x: print(x)
                    )
                ])
        ])
        def fct_description_callback(a):
            return a

        self.functions = [fct, fct_description, fct_description_callback]

    def test_correct(self):
        for f in self.functions:
            f(3)
            f(6)
            f(9)

    def test_check1_err(self):
        for f in self.functions:
            try:
                f(2)
                self.assertTrue(False)   # should have raised an exception
            except fg.exceptions.ParameterGuaranteesValueError:
                self.assertTrue(True)    # successfully raised exception

    def test_check2_err(self):
        for f in self.functions:
            try:
                f(3**10)
                self.assertTrue(False)  # should have raised an exception
            except fg.exceptions.ParameterGuaranteesValueError:
                self.assertTrue(True)   # successfully raised exception


class ClassWithMethods:
    def __init__(self):
        self.const = 1

    @fg.add_guarantees(param_guarantees=[fg.IsInt("a")])
    def fct(self, a):
        return a + self.const

    @classmethod
    @fg.add_guarantees(param_guarantees=[fg.IsInt("a")])
    def classfct(cls, a):
        return a

    @staticmethod
    @fg.add_guarantees(is_staticmethod=True, param_guarantees=[fg.IsInt("a")])
    def staticfct(a):
        return a


class TestMethodGuarantees(unittest.TestCase):
    def setUp(self) -> None:
        self.class_with_methods = ClassWithMethods()

    def test_self_correct(self):
        val = self.class_with_methods.fct(3)
        self.assertIsInstance(val, int)

    def test_self_error(self):
        try:
            self.class_with_methods.fct("not an int!")
            self.assertTrue(False)    # should have raised an exception
        except fg.exceptions.ParameterGuaranteesTypeError:
            self.assertTrue(True)

    def test_cls_correct(self):
        val = self.class_with_methods.classfct(3)
        self.assertIsInstance(val, int)

    def test_cls_error(self):
        try:
            self.class_with_methods.classfct("not an int")
            self.assertTrue(False)   # should have raised an exception
        except fg.exceptions.ParameterGuaranteesTypeError:
            self.assertTrue(True)

    def test_static_correct(self):
        val = self.class_with_methods.staticfct(3)
        self.assertIsInstance(val, int)

    def test_static_error(self):
        try:
            self.class_with_methods.staticfct("not an int")
            self.assertTrue(False)   # should have raised an exception
        except fg.exceptions.ParameterGuaranteesTypeError:
            self.assertTrue(True)


class TestReturnGuarantees(unittest.TestCase):
    def test_correct(self) -> None:
        @fg.add_guarantees(return_guarantee=fg.IsInt("a"))
        def fct(a):
            return a

        ret_val = fct(1)
        self.assertIsInstance(ret_val, int)

    def test_false(self):
        @fg.add_guarantees(return_guarantee=fg.IsInt("a"))
        def fct(a):
            return float(a)

        try:
            fct(1)
            self.assertTrue(False)   # should have raised an exception
        except fg.exceptions.ReturnGuaranteesTypeError:
            self.assertTrue(True)    # successfully raised an exception

    def test_false_with_conversion(self):
        @fg.add_guarantees(return_guarantee=fg.IsInt("a", force_conversion=True))
        def fct(a):
            return float(a)

        ret_val = fct(1)
        self.assertIsInstance(ret_val, int)
