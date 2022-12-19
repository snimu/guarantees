import logging
import pytest

import pyguarantees as pg
from pyguarantees.constraints import IsInt


logger_called = False


class Logger(logging.Logger):
    def __init__(self):
        super().__init__("testLogger")

    def debug(self, *args, **kwargs) -> None:
        global logger_called
        logger_called = True

    def info(self, *args, **kwargs) -> None:
        global logger_called
        logger_called = True

    def warning(self, *args, **kwargs) -> None:
        global logger_called
        logger_called = True

    def error(self, *args, **kwargs) -> None:
        global logger_called
        logger_called = True

    def critical(self, *args, **kwargs) -> None:
        global logger_called
        logger_called = True


@pg.constrain.parameters(a=IsInt(logger=Logger(), logger_only=True))
def fct_logger_only(a):
    return a


@pg.constrain.parameters(a=IsInt(logger=Logger()))
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

    def test_debug_levels(self):
        global logger_called
        severity = [pg.severity.DEBUG, pg.severity.INFO, pg.severity.WARNING]

        for severity in severity:
            @pg.constrain.parameters(a=IsInt(logger=Logger(), error_severity=severity))
            def fct(a):
                return a

            # Cause error output
            fct("not an int")
            assert logger_called
            logger_called = False

    def test_critical(self):
        @pg.constrain.parameters(a=IsInt(logger=Logger(), error_severity=pg.severity.CRITICAL))
        def fct(a):
            return a

        with pytest.raises(pg.exceptions.constraints.ParameterGuaranteesTypeError):
            fct("not an int")

        global logger_called
        logger_called = False
