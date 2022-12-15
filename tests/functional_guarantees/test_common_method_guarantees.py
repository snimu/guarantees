import pytest

from pyguarantees import functional_guarantees as fg


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


class_with_methods = ClassWithMethods()


class TestMethodGuarantees:
    def test_self_correct(self):
        val = class_with_methods.fct(3)
        assert isinstance(val, int)

    def test_self_error(self):
        with pytest.raises(fg.exceptions.ParameterGuaranteesTypeError):
            class_with_methods.fct("not an int!")

    def test_cls_correct(self):
        val = class_with_methods.classfct(3)
        assert isinstance(val, int)

    def test_cls_error(self):
        with pytest.raises(fg.exceptions.ParameterGuaranteesTypeError):
            class_with_methods.classfct("not an int!")

    def test_static_correct(self):
        val = class_with_methods.staticfct(3)
        assert isinstance(val, int)

    def test_static_error(self):
        with pytest.raises(fg.exceptions.ParameterGuaranteesTypeError):
            class_with_methods.staticfct("not an int!")
