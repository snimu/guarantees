import pytest
import pyguarantees as pg
from pyguarantees.constraints import Self


class NotAConstraint:
    pass


class BadClass:
    @pg.constrain.parameters(Self(), a=NotAConstraint())
    def bad_parameter_constraint(self, a):
        return a

    @pg.constrain.parameters(NotAConstraint())
    def bad_self(self):
        return "hi"

    @pg.constrain.returns(NotAConstraint())
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


