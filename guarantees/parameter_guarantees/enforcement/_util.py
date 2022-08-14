import warnings
from typing import Any

from guarantees.parameter_guarantees.classes import TypeGuarantee, IsInt, \
    IsFloat, IsComplex, IsBool, IsDict, IsSet, IsFrozenSet, IsStr, IsList, \
    IsRange, IsTuple, IsClass, IsBytes, IsByteArray, IsMemoryView
from guarantees.parameter_guarantees.signals.base import SignalTypeError


guarantee_to_type_dict = {
    IsInt: int,
    IsFloat: float,
    IsComplex: complex,
    IsBool: bool,
    IsStr: str,
    IsList: list,
    IsTuple: tuple,
    IsDict: dict,
    IsSet: set,
    IsFrozenSet: frozenset,
    IsRange: range,
    IsClass: object,
    IsBytes: bytes,
    IsByteArray: bytearray,
    IsMemoryView: memoryview
}


guarantee_to_type_name_dict = {
    IsInt: "int",
    IsFloat: "float",
    IsComplex: "complex",
    IsBool: "bool",
    IsStr: "str",
    IsList: "list",
    IsTuple: "tuple",
    IsDict: "dict",
    IsSet: "set",
    IsFrozenSet: "frozenset",
    IsRange: "range",
    IsClass: "object",
    IsBytes: "bytes",
    IsByteArray: "bytearray",
    IsMemoryView: "memoryview"
}


def get_guaranteed_type(type_guarantee: TypeGuarantee):
    global guarantee_to_type_dict
    return guarantee_to_type_dict[type(type_guarantee)]


def get_guaranteed_type_name(type_guarantee: TypeGuarantee):
    global guarantee_to_type_name_dict
    return guarantee_to_type_name_dict[type(type_guarantee)]


type_to_str_dict = {
    int: "int",
    float: "float",
    complex: "complex",
    bool: "bool",
    str: "str",
    list: "list",
    tuple: "tuple",
    dict: "dict",
    set: "set",
    frozenset: "frozenset",
    bytes: "bytes",
    bytearray: "bytearray",
    memoryview: "memoryview",
    range: "range"
}


def get_type_name(parameter: Any) -> str:
    try:
        global type_to_str_dict
        return type_to_str_dict[type(parameter)]
    except KeyError:
        return str(type(parameter))


guarantee_name_dict = {
    IsInt: "IsInt",
    IsFloat: "IsFloat",
    IsComplex: "IsComplex",
    IsBool: "IsBool",
    IsStr: "IsStr",
    IsList: "IsList",
    IsTuple: "IsTuple",
    IsDict: "IsDict",
    IsSet: "IsSet",
    IsFrozenSet: "IsFrozenSet",
    IsRange: "IsRange",
    IsClass: "IsClass",
    IsBytes: "IsBytes",
    IsByteArray: "IsByteArray",
    IsMemoryView: "IsMemoryView"
}


def get_guarantee_name(type_guarantee: TypeGuarantee) -> str:
    global guarantee_name_dict
    return guarantee_name_dict[type(type_guarantee)]


# TODO (snimu) Redesign Signals:
#   SignalSettingError for things like min_ge_max
#       - parameter_name
#       - should     (the should-value)
#       - actual     (the is-value)
#   SignalParameterError for things like arg < minimum
# TODO (snimu) Redesign getting of error-msg:
#   All necessary information in Signal
#   For SignalSettingError: just receive Signal
#   For SignalParameterError: also receive arg
#   Error msg design:
#       For SignalSettingError:
#           "settings:
#                   - ...
#                   - ...
#               should:     (in text form)
#               actual:     (in text form)"
#       For SignalParameterError:
#           "parameter:
#                   - <parameter name>
#               should: ...
#               actual:     ..."


def get_err_msg_type(signal: SignalTypeError) -> str:
    err_msg = f"parameter: {signal.parameter_name} \n" \
              f"\t guarantee: type \n" \
              f"\t type should: {signal.should_type_name} \n" \
              f"\t type is:     {signal.is_type_name} \n" \
              f"\t force_conversion: {signal.force_conversion} \n"

    return err_msg


def get_err_msg_minimum_len_type(
        type_guarantee: TypeGuarantee
) -> str:
    err_msg = f"parameter: {get_guarantee_name(type_guarantee)}.mimimum_len\n" \
              f"\t type should: {int} \"" \
              f"\t type is:     {get_guaranteed_type(type_guarantee)} \n"

    return err_msg


def get_err_msg_maximum_len_type(
        type_guarantee: TypeGuarantee
) -> str:
    err_msg = f"parameter: {get_guarantee_name(type_guarantee)}.maximum_len\n" \
              f"\t type should: {int} \"" \
              f"\t type is:     {get_guaranteed_type(type_guarantee)} \n"

    return err_msg


def get_err_msg_minimum_ge_maximum(
        type_guarantee: TypeGuarantee,
        minimum_len: int,
        maximum_len: int
) -> str:
    err_msg = f"paramter: {get_guarantee_name(type_guarantee)}.minimum_len " \
              f"and {get_guarantee_name(type_guarantee)}.maximum_len \"" \
              f"\t minimum_len ({minimum_len}) " \
              f">= maximum_len ({maximum_len}) \n"

    return err_msg


def get_err_msg_minimum_len(
        type_guarantee: TypeGuarantee,
        minimum_len: int,
        actual_len: int
) -> str:
    err_msg = f"parameter: {get_guarantee_name(type_guarantee)}.minimum_len " \
              f"\t len should : >= {minimum_len} \n" \
              f"\t len is     :    {actual_len}"

    return err_msg


def get_err_msg_maximum_len(
        type_guarantee: TypeGuarantee,
        maximum_len: int,
        actual_len: int
) -> str:
    err_msg = f"parameter: {get_guarantee_name(type_guarantee)}.maximum_len " \
              f"\t len should : >= {maximum_len} \n" \
              f"\t len is     :    {actual_len}"

    return err_msg


def raise_type_warning_or_exception(
        err_msg: str,
        type_guarantee: TypeGuarantee
) -> None:
    if type_guarantee.warnings_only:
        warnings.warn(err_msg + "\t **Ignoring**")
    else:
        raise TypeError(err_msg)


def raise_value_warning_or_exception(
        err_msg: str,
        type_guarantee: TypeGuarantee
) -> None:
    if type_guarantee.warnings_only:
        warnings.warn(err_msg + "\t **Ignoring**")
    else:
        raise ValueError(err_msg)

