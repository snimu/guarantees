from typing import Union

from guarantees.functional_guarantees.classes import IsBytes, \
    IsByteArray, IsMemoryView
from guarantees.functional_guarantees.enforcement._util import \
    get_guarantee_name, get_guaranteed_type, get_type_name, \
    get_guaranteed_type_name, get_err_msg_type, \
    raise_warning_or_exception, choose_exception, raise_type_warning_or_exception
from guarantees.functional_guarantees.signals.common import SignalTypeError


def enforce_isbytes(arg: bytes, guarantee: IsBytes) -> bytes:
    arg = _check_type(arg, guarantee)

    if guarantee.check_function is not None:
        arg = guarantee.check_function(arg)
    return arg


def enforce_isbytearray(arg: bytearray, guarantee: IsByteArray) -> bytearray:
    arg = _check_type(arg, guarantee)

    if guarantee.check_function is not None:
        arg = guarantee.check_function(arg)
    return arg


def enforce_ismemoryview(
        arg: memoryview,
        guarantee: IsMemoryView
) -> memoryview:
    arg = _check_type(arg, guarantee)

    if guarantee.check_function is not None:
        arg = guarantee.check_function(arg)
    return arg


def _check_type(
        arg: Union[bytes, bytearray, memoryview],
        guarantee: Union[IsBytes, IsByteArray, IsMemoryView]
) -> Union[bytes, bytearray, memoryview]:
    type_should = get_guaranteed_type(guarantee)

    if isinstance(arg, type_should):
        return arg

    if guarantee.force_conversion:
        try:
            return type_should(arg)
        except TypeError:
            pass

    # Type error occurred
    exception = choose_exception(where=guarantee.where, what="type")
    exception = exception(
        function_name=guarantee.function_name,
        function_namespace=guarantee.function_namespace,
        guarantee_type_name=get_guaranteed_type_name(guarantee),
        what_dict={
            "should_type_name": get_guaranteed_type_name(guarantee),
            "actual_type_name": get_type_name(arg)
        }
    )

    if guarantee.error_callback is not None:
        guarantee.error_callback(exception)
    else:
        raise_warning_or_exception(exception, guarantee)

    return arg   # in case of warnings_only
