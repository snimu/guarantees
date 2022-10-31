import unittest
from guarantees import functional_guarantees as fg


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
                check_functions=[
                    lambda x: x % 3 == 0,
                    lambda x: x ** 2 - 2 * x < 1e4
                ])
        ])
        def fct_list(a):
            return a

        @fg.add_guarantees(param_guarantees=[
            fg.IsInt(
                "a",
                check_functions={
                    "divisible by 3": lambda x: x % 3 == 0,
                    "on correct side of decision boundary":
                        lambda x: x**2 - 2 * x < 1e4
                })
        ])
        def fct_dict_str_fct(a):
            return a

        @fg.add_guarantees(param_guarantees=[
            fg.IsInt(
                "a",
                check_functions={
                    lambda x: x % 3 == 0: "divisible by 3",
                    lambda x: x**2 - 2 * x < 1e4:
                        "on correct side of decision boundary"
                })
        ])
        def fct_dict_fct_str(a):
            return a

        self.fct_list = fct_list
        self.fct_dict_str_fct = fct_dict_str_fct
        self.fct_dict_fct_str = fct_dict_fct_str

    def test_list_isint_correct(self):
        self.fct_list(3)
        self.fct_list(9)

    def test_list_isint_error_fct_1(self):
        try:
            self.fct_list(2)         # not divisible by 3
            self.assertTrue(False)   # should have raised an exception
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)    # successfully raised an exception

    def test_list_isint_error_fct_2(self):
        try:
            self.fct_list(3**10)     # divisible by 3, but too large
            self.assertTrue(False)   # should have raised an exception
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)    # successfully raised an exception

    def test_dict_str_fct_isint_correct(self):
        ret = self.fct_dict_str_fct(3)
        self.assertIsInstance(ret, int)

        ret = self.fct_dict_str_fct(9)
        self.assertIsInstance(ret, int)

    def test_dict_str_fct_isint_error_1(self):
        try:
            self.fct_dict_str_fct(2)
            self.assertTrue(False)
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)

    def test_dict_str_fct_isint_error_2(self):
        try:
            self.fct_dict_str_fct(3 ** 10)
            self.assertTrue(False)
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)

    def test_dict_fct_str_isint_correct(self):
        ret = self.fct_dict_fct_str(3)
        self.assertIsInstance(ret, int)

        ret = self.fct_dict_fct_str(9)
        self.assertIsInstance(ret, int)

    def test_dict_fct_str_isint_error_1(self):
        try:
            self.fct_dict_fct_str(2)
            self.assertTrue(False)
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)

    def test_dict_fct_str_isint_error_2(self):
        try:
            self.fct_dict_fct_str(3 ** 10)
            self.assertTrue(False)
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)


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



