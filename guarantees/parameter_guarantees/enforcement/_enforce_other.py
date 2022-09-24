from typing import Any

from guarantees.parameter_guarantees.classes import IsClass, IsNone
from guarantees.parameter_guarantees.signals.common import SignalTypeError
from guarantees.parameter_guarantees.enforcement._util import \
    get_guarantee_name, get_type_name, get_err_msg_type, \
    raise_type_warning_or_exception


# NoOp needs no enforcement; it is handled in the guarantee_handler
def enforce_isclass(arg: object, guarantee: IsClass) -> object:
    arg = _check_isclass(arg, guarantee)
    if guarantee.check_fct is not None:
        return guarantee.check_fct(arg)
    return arg


def enforce_isnone(arg: None, guarantee: IsNone) -> None:
    if arg is None:
        return

    signal = SignalTypeError(
        parameter_name=guarantee.parameter_name,
        guarantee_type_name=get_guarantee_name(guarantee),
        should_type_name="None",
        is_type_name=get_type_name(arg)
    )
    if guarantee.error_callback is not None:
        guarantee.error_callback(signal)
    else:
        err_msg = get_err_msg_type(signal)
        raise_type_warning_or_exception(err_msg, guarantee)


def _check_isclass(arg: object, guarantee: IsClass) -> object:
    if guarantee.class_type is None or isinstance(arg, guarantee.class_type):
        return arg

    signal = SignalTypeError(
        parameter_name=guarantee.parameter_name,
        guarantee_type_name=get_guarantee_name(guarantee),
        should_type_name=get_type_name(guarantee.class_type),
        is_type_name=get_type_name(arg)
    )
    if guarantee.error_callback is not None:
        guarantee.error_callback(signal)
    else:
        err_msg = get_err_msg_type(signal)
        raise_type_warning_or_exception(err_msg, guarantee)
