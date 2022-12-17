import pytest

import pyguarantees as pg
from pyguarantees.constraints import IsInt


class ClassWithMethods:
    def __init__(self):
        self.const = 1

    @pg.constrain.add_guarantees(param_guarantees=[IsInt("a")])
    def fct(self, a):
        return a + self.const

    @classmethod
    @pg.constrain.add_guarantees(param_guarantees=[IsInt("a")])
    def classfct(cls, a):
        return a

    @staticmethod
    @pg.constrain.add_guarantees(is_staticmethod=True, param_guarantees=[IsInt("a")])
    def staticfct(a):
        return a


class_with_methods = ClassWithMethods()


class TestMethodGuarantees:
    def test_self_correct(self):
        val = class_with_methods.fct(3)
        assert isinstance(val, int)

    def test_self_error(self):
        with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesTypeError):
            class_with_methods.fct("not an int!")

    def test_cls_correct(self):
        val = class_with_methods.classfct(3)
        assert isinstance(val, int)

    def test_cls_error(self):
        with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesTypeError):
            class_with_methods.classfct("not an int!")

    def test_static_correct(self):
        val = class_with_methods.staticfct(3)
        assert isinstance(val, int)

    def test_static_error(self):
        with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesTypeError):
            class_with_methods.staticfct("not an int!")
