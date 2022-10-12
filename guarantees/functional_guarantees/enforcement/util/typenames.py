from typing import Any

from guarantees.functional_guarantees.classes import TypeGuarantee, IsInt, \
    IsFloat, IsComplex, IsBool, IsDict, IsSet, IsFrozenSet, IsStr, IsList, \
    IsRange, IsTuple, IsClass, IsBytes, IsByteArray, IsMemoryView, IsNone, \
    IsUnion

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
    IsMemoryView: memoryview,
    IsNone: None,
    IsUnion: Any
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
    IsMemoryView: "memoryview",
    IsNone: "None",
    IsUnion: "Union"
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
    range: "range",
    None: "None"
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
    IsMemoryView: "IsMemoryView",
    IsNone: "IsNone",
    IsUnion: "IsUnion"
}


def get_guarantee_name(type_guarantee: TypeGuarantee) -> str:
    global guarantee_name_dict
    return guarantee_name_dict[type(type_guarantee)]
