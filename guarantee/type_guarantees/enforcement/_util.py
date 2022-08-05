import warnings
from typing import Any

from guarantee.type_guarantees.guarantees import TypeGuarantee, IsInt, \
    IsFloat, IsComplex, IsBool, IsDict, IsSet, IsFrozenSet, IsStr, IsList, \
    IsRange, IsTuple, IsClass, IsBytes, IsByteArray, IsMemoryView
from guarantee.type_guarantees.signals.base import SignalTypeError


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


def get_err_msg_type(signal: SignalTypeError) -> str:
    err_str = f"parameter: {signal.parameter_name} \n" \
              f"\t guarantee: type \n" \
              f"\t type should: {signal.should_type_name} \n" \
              f"\t type is:     {signal.is_type_name} \n" \
              f"\t force_conversion: {signal.force_conversion} \n"

    return err_str


def get_err_msg_minimum_len_type(
        type_guarantee: TypeGuarantee
) -> str:
    err_str = f"parameter: {get_guarantee_name(type_guarantee)}.mimimum_len\n" \
              f"\t type should: {int} \"" \
              f"\t type is:     {get_guaranteed_type(type_guarantee)} \n"

    return err_str


def get_err_msg_maximum_len_type(
        type_guarantee: TypeGuarantee
) -> str:
    err_str = f"parameter: {get_guarantee_name(type_guarantee)}.maximum_len\n" \
              f"\t type should: {int} \"" \
              f"\t type is:     {get_guaranteed_type(type_guarantee)} \n"

    return err_str


def raise_warning_or_exception(
        err_msg: str,
        type_guarantee: TypeGuarantee
) -> None:
    if type_guarantee.warnings_only:
        warnings.warn(err_msg + "\t **Ignoring**")
    else:
        raise TypeError(err_msg)

