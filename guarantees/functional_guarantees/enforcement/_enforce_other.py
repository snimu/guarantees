from typing import Any

from guarantees.functional_guarantees.classes import IsClass, IsNone
from guarantees.functional_guarantees.signals.common import SignalTypeError
from guarantees.functional_guarantees.enforcement._util import \
    get_type_name, handle_error


# NoOp needs no enforcement; it is handled in the guarantee_handler
def enforce_isclass(arg: object, guarantee: IsClass) -> object:
    arg = _check_isclass(arg, guarantee)

    if guarantee.check_function is not None:
        arg = guarantee.check_function(arg)
    return arg


def enforce_isnone(arg: None, guarantee: IsNone) -> None:
    if arg is None:
        return

    handle_error(
        where=guarantee.where,
        type_or_value="type",
        guarantee=guarantee,
        parameter_name=guarantee.parameter_name,
        what_dict={
            "should_type": "None",
            "actual_type": get_type_name(arg)
        }
    )


def _check_isclass(arg: object, guarantee: IsClass) -> object:
    if guarantee.class_type is None or isinstance(arg, guarantee.class_type):
        return arg

    handle_error(
        where=guarantee.where,
        type_or_value="type",
        guarantee=guarantee,
        parameter_name=guarantee.parameter_name,
        what_dict={
            "should_type": str(guarantee.class_type),
            "actual_type": get_type_name(arg)
        }
    )
