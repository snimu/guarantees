import logging
import pytest

import pyguarantees as pg
from pyguarantees.constraints import IsInt


logger_called = False


class Logger(logging.Logger):
    def __init__(self):
        super().__init__("testLogger")

    def error(self, *args, **kwargs) -> None:
        global logger_called
        logger_called = True


@pg.constrain.add_guarantees(
    param_guarantees=[
        IsInt("a", logger=Logger(), logger_only=True)
    ]
)
def fct_logger_only(a):
    return a


@pg.constrain.add_guarantees(param_guarantees=[IsInt("a", logger=Logger())])
def fct_logger_and_error(a):
    return a


class TestLogger:
    def test_logger_only(self):
        fct_logger_only(3.)   # not an int

        global logger_called
        assert logger_called
        logger_called = False   # reset for other tests

    def test_logger_and_error(self):
        with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesTypeError):
            fct_logger_and_error(3.)

        global logger_called
        assert logger_called
        logger_called = False
