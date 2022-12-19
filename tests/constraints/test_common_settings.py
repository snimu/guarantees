import pytest
import pyguarantees as pg
from pyguarantees.constraints import IsInt


def test_onoff():
    @pg.constrain.parameters(a=IsInt())
    def fct_param(a):
        return a

    @pg.constrain.returns(IsInt())
    def fct_ret(a):
        return a

    # Check that it works in general
    val = fct_param(1)
    assert val == 1

    val = fct_ret(1)
    assert val == 1

    with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesTypeError):
        fct_param("not an int!")
    with pytest.raises(pg.exceptions.constraints.ReturnGuaranteesTypeError):
        fct_ret("not and int!")

    # Shouldn't raise an exception when off
    pg.settings.change_settings(active=False)
    fct_param("not an int!")
    fct_ret("not an int!")

    # Turn on again
    pg.settings.change_settings(active=True)
    with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesTypeError):
        fct_param("not an int!")
    with pytest.raises(pg.exceptions.constraints.ReturnGuaranteesTypeError):
        fct_ret("not and int!")


def test_cache():
    @pg.constrain.parameters(a=IsInt())
    @pg.constrain.returns(IsInt())
    def fct(a):
        return a

    assert fct(1) == 1
    assert pg._constrain._guarantee_handler.ParameterHandler.handles != {}   # Guarantee should be saved
    assert pg._constrain._guarantee_handler.ReturnHandler.handles != {}

    pg.settings.change_settings(cache=False)
    assert pg._constrain._guarantee_handler.ParameterHandler.handles == {}
    assert pg._constrain._guarantee_handler.ReturnHandler.handles == {}
    assert fct(1) == 1

    pg.settings.change_settings(cache=True)
    assert fct(1) == 1
    assert pg._constrain._guarantee_handler.ParameterHandler.handles != {}
    assert pg._constrain._guarantee_handler.ReturnHandler.handles != {}
