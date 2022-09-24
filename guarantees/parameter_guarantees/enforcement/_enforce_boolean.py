from guarantees.parameter_guarantees.classes import IsBool
from guarantees.parameter_guarantees.signals.common import SignalTypeError
from guarantees.parameter_guarantees.enforcement._util import \
    get_type_name, get_err_msg_type, raise_type_warning_or_exception


def enforce_isbool(arg: bool, guarantee: IsBool) -> bool:
    arg = _check_type(arg, guarantee)

    if guarantee.check_function is not None:
        arg = guarantee.check_function(arg)
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

    if not err:
        return arg

    signal = SignalTypeError(
        parameter_name=guarantee.parameter_name,
        guarantee_type_name="IsBool",
        should_type_name="bool",
        is_type_name=get_type_name(arg)
    )
    if guarantee.error_callback is not None:
        guarantee.error_callback(signal)
    else:
        err_msg = get_err_msg_type(signal)
        raise_type_warning_or_exception(err_msg, guarantee)
