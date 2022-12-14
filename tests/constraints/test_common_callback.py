import pytest

import pyguarantees as pg
from pyguarantees.constraints import (
    IsInt,
    IsStr,
    IsList
)


class CbException(Exception):
    pass


def cb(signal):
    raise CbException(f"success: {signal}")


@pg.constrain.parameters(
    a=IsInt(error_callback=cb),
    b=IsStr(error_callback=cb),
    c=IsList(error_callback=cb)
)
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
