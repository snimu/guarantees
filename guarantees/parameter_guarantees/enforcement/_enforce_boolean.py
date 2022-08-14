import warnings

from guarantees.parameter_guarantees.classes import IsBool
from guarantees.parameter_guarantees.signals.base import SignalTypeError


def enforce_isbool(arg: bool, guarantee: IsBool) -> bool:
    arg = _check_type(arg, guarantee)
    return arg


def _check_type(arg: bool, guarantee: IsBool) -> bool:
    err = False

    if guarantee.force_conversion:
        try:
            arg = bool(arg)
        except ValueError:
            err = True
    else:
        if type(arg) is not bool:
            err = True

    if err:
        if guarantee.callback is not None:
            guarantee.callback(
                SignalTypeError(
                    arg_name=guarantee.parameter_name,
                    type_should="bool",
                    type_is=str(type(arg)),
                    force_conversion=guarantee.force_conversion
                )
            )
        else:
            err_msg = f"Guaranteed type bool " \
                      f"for parameter {guarantee.parameter_name}, " \
                      f"but received type {type(arg)}. " \
                      f"Called with " \
                      f"force_conversion={guarantee.force_conversion}. "
            if guarantee.warnings_only:
                warnings.warn(err_msg + "Ignoring.")
            else:
                raise TypeError(err_msg)

    return arg
