import pytest
import pyguarantees as pg
from pyguarantees.constraints import IsInt


def test_onoff():
    @pg.constrain.parameters(a=IsInt())
    def fct(a):
        return a

    # Check that it works in general
    val = fct(1)
    assert isinstance(val, int)

    with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesTypeError):
        fct("not an int!")

    # Shouldn't raise an exception when off
    pg.settings.change_settings(active=False)
    fct("not an int!")

    # Turn on again
    pg.settings.change_settings(active=True)
    with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesTypeError):
        fct("not an int!")


def test_cache():
    @pg.constrain.parameters(a=IsInt())
    def fct(a):
        return a

    assert fct(1) == 1
    assert pg._constrain._guarantee_handler.ParameterHandler.handles != {}   # Guarantee should be saved

    pg.settings.change_settings(cache=False)
    assert pg._constrain._guarantee_handler.ParameterHandler.handles == {}
    assert fct(1) == 1

    pg.settings.change_settings(cache=True)
    assert fct(1) == 1
    assert pg._constrain._guarantee_handler.ParameterHandler.handles != {}
