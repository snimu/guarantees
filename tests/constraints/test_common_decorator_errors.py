import pytest
import pyguarantees as pg
from pyguarantees.constraints import Self


class BadClass:
    @pg.constrain.parameters(Self(), a=1)
    def bad_parameter_constraint(self, a):
        return a

    @pg.constrain.parameters(1)
    def bad_self(self):
        return "hi"

    @pg.constrain.returns(1)
    def bad_return_constraint(self):
        return "hi"


def test_bad_parameter_constraint():
    with pytest.raises(pg.exceptions.constraints.FunctionalGuaranteesUserTypeError):
        BadClass().bad_parameter_constraint(1)


def test_bad_self():
    with pytest.raises(pg.exceptions.constraints.FunctionalGuaranteesUserTypeError):
        BadClass().bad_self()


def test_bad_return_constraint():
    with pytest.raises(pg.exceptions.constraints.FunctionalGuaranteesUserTypeError):
        BadClass().bad_return_constraint()


