import pytest
from pyguarantees import functional_guarantees as fg


def test_onoff():
    @fg.add_guarantees(param_guarantees=[fg.IsInt("a")])
    def fct(a):
        return a

    # Check that it works in general
    val = fct(1)
    assert isinstance(val, int)

    with pytest.raises(fg.exceptions.ParameterGuaranteesTypeError):
        fct("not an int!")

    # Shouldn't raise an exception when off
    fg.settings.change_settings(active=False)
    fct("not an int!")

    # Turn on again
    fg.settings.change_settings(active=True)
    with pytest.raises(fg.exceptions.ParameterGuaranteesTypeError):
        fct("not an int!")


def test_cache():
    @fg.add_guarantees(param_guarantees=[fg.IsInt("a")])
    def fct(a):
        return a

    assert fct(1) == 1
    assert fg.decorator._guarantee_handler.ParameterHandler.handles != {}   # Guarantee should be saved

    fg.settings.change_settings(cache=False)
    assert fg.decorator._guarantee_handler.ParameterHandler.handles == {}
    assert fct(1) == 1

    fg.settings.change_settings(cache=True)
    assert fct(1) == 1
    assert fg.decorator._guarantee_handler.ParameterHandler.handles != {}