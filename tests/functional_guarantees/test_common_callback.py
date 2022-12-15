import pytest

from pyguarantees import functional_guarantees as fg


class CbException(Exception):
    pass


def cb(signal):
    raise CbException(f"success: {signal}")


@fg.add_guarantees(param_guarantees=[
    fg.IsInt("a", error_callback=cb),
    fg.IsStr("b", error_callback=cb),
    fg.IsList("c", error_callback=cb)
])
def fct(a, b, c):
    return a, b, c


class TestCallback:
    def test_isint_cb(self):
        with pytest.raises(CbException):
            fct(1., "hi", [])

    def test_isstr_cb(self):
        with pytest.raises(CbException):
            fct(1, 1, [])

    def test_islist_cb(self):
        with pytest.raises(CbException):
            fct(1, "hi", 1)
