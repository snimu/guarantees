from typing import Union

from guarantees.functional_guarantees.classes import IsBytes, \
    IsByteArray, IsMemoryView
from guarantees.functional_guarantees.enforcement.util.typenames import \
    get_guaranteed_type, get_type_name, get_guaranteed_type_name
from guarantees.functional_guarantees.enforcement.util.error_handeling import \
    handle_error


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
    handle_error(
        where=guarantee.where,
        type_or_value="type",
        guarantee=guarantee,
        parameter_name=guarantee.parameter_name,
        what_dict={
            "should_type": get_guaranteed_type_name(guarantee),
            "actual_type": get_type_name(arg)
        }
    )

    return arg   # in case of warnings_only
