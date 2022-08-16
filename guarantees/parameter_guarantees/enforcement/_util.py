import warnings
from typing import Any

from guarantees.parameter_guarantees.classes import TypeGuarantee, IsInt, \
    IsFloat, IsComplex, IsBool, IsDict, IsSet, IsFrozenSet, IsStr, IsList, \
    IsRange, IsTuple, IsClass, IsBytes, IsByteArray, IsMemoryView
from guarantees.parameter_guarantees.signals.base import SignalTypeError
from guarantees.parameter_guarantees.signals.collections import \
    SignalMinLenGEMaxLen, SignalMinLenViolated, SignalMaxLenViolated, \
    SignalContainsViolated, SignalHasKeysViolated, SignalHasValuesViolated
from guarantees.parameter_guarantees.signals.numeric import SignalMinGEMax, \
    SignalMinReGEMaxRe, SignalMinImGEMaxIm, SignalMinViolated, \
    SignalMinReViolated, SignalMinImViolated, SignalMaxViolated, \
    SignalMaxReViolated, SignalMaxImViolated, SignalNotIn


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
    err_msg = f"parameter: {signal.parameter_name} \n" \
              f"\t violated         : type -- parameter \n" \
              f"\t should           : {signal.should_type_name} \n" \
              f"\t actual           :     {signal.is_type_name} \n" \
              f"\t force_conversion : {signal.force_conversion} \n"

    return err_msg


def get_err_msg_minimum_len_type(signal: SignalTypeError) -> str:
    err_msg = f"parameter: {signal.guarantee_type_name}.mimimum_len \n" \
              f"\t violated : type -- guarantee parameter" \
              f".minimum_len \n" \
              f"\t should   : {signal.should_type_name} \n" \
              f"\t actual   :     {signal.is_type_name} \n"

    return err_msg


def get_err_msg_maximum_len_type(signal: SignalTypeError) -> str:
    err_msg = f"parameter: {signal.guarantee_type_name}.maximum_len\n" \
              f"\t violated : type -- guarantee parameter" \
              f".maximum_len \n" \
              f"\t should   : {signal.should_type_name} \n" \
              f"\t actual   :     {signal.is_type_name} \n"

    return err_msg


def get_err_msg_minimum_len_ge_maximum_len(signal: SignalMinLenGEMaxLen) -> str:
    err_msg = f"paramter: {signal.guarantee_type_name}.minimum_len " \
              f"and {signal.guarantee_type_name}.maximum_len \n" \
              f"\t violated    : minimum_len < maximum_len \n" \
              f"\t minimum_len : {signal.minimum_len} \n" \
              f"\t maximum_len : {signal.maximum_len} \n"

    return err_msg


def get_err_msg_minimum_len(signal: SignalMinLenViolated) -> str:
    err_msg = f"parameter: {signal.parameter_name} \n" \
              f"\t violated : {signal.guarantee_type_name}.minimum_len \n" \
              f"\t should   : >= {signal.minimum_len} \n" \
              f"\t actual   :    {len(signal.arg)} \n"

    return err_msg


def get_err_msg_maximum_len(signal: SignalMaxLenViolated) -> str:
    err_msg = f"parameter: {signal.parameter_name} \n" \
              f"\t violated : {signal.guarantee_type_name}.maximum_len \n" \
              f"\t should   : >= {signal.maximum_len} \n" \
              f"\t actual   :    {len(signal.arg)} \n"

    return err_msg


def get_err_msg_contains(signal: SignalContainsViolated) -> str:
    err_msg = f"parameter: {signal.parameter_name} \n" \
              f"\t violated : {signal.guarantee_type_name}.contains \n" \
              f"\t should   : {signal.contains} \n" \
              f"\t actual   : {signal.arg} \n"

    return err_msg


def get_err_msg_has_keys(signal: SignalHasKeysViolated) -> str:
    err_msg = f"parameter: {signal.parameter_name} \n" \
              f"\t violated : {signal.guarantee_type_name}.has_keys \n" \
              f"\t should   : {signal.has_keys} \n" \
              f"\t actual   : {signal.arg} \n"

    return err_msg


def get_err_msg_has_values(signal: SignalHasValuesViolated) -> str:
    err_msg = f"parameter: {signal.parameter_name} \n" \
              f"\t violated : {signal.guarantee_type_name}.has_values \n" \
              f"\t should   : {signal.has_values} \n" \
              f"\t actual   : {signal.arg} \n"

    return err_msg


def get_err_msg_minimum_ge_maximum(signal: SignalMinGEMax) -> str:
    minstr, maxstr = "minimum", "maximum"
    if isinstance(signal, SignalMinReGEMaxRe):
        minstr, maxstr = "minimum_re", "maximum_re"
    if isinstance(signal, SignalMinImGEMaxIm):
        minstr, maxstr = "minimum_im", "maximum_im"

    err_msg = f"parameter: {signal.guarantee_type_name}.{minstr} and " \
              f"{signal.guarantee_type_name}.{maxstr} \n" \
              f"\t violated : minimum < maximum \n" \
              f"\t minimum  : {signal.minimum} \n" \
              f"\t maximum  : {signal.maximum} \n"

    return err_msg


def get_err_msg_minimum(signal: SignalMinViolated) -> str:
    minstr = "minimum"
    if isinstance(signal, SignalMinReViolated):
        minstr = "minimum_re"
    if isinstance(signal, SignalMinImViolated):
        minstr = "minimum_im"

    err_msg = f"parameter: {signal.guarantee_type_name}.{minstr} \n" \
              f"\t violated : type -- guarantee parameter \n" \
              f"\t should   : >= {signal.minimum} \n" \
              f"\t actual   :    {signal.arg} \n"

    return err_msg


def get_err_msg_maximum(signal: SignalMaxViolated) -> str:
    maxstr = "maximum"
    if isinstance(signal, SignalMinReViolated):
        maxstr = "maximum_re"
    if isinstance(signal, SignalMinImViolated):
        maxstr = "maximum_im"

    err_msg = f"parameter: {signal.guarantee_type_name}.{maxstr} \n" \
              f"\t violated : type -- guarantee parameter \n" \
              f"\t should   : <= {signal.maximum} \n" \
              f"\t actual   :    {signal.arg} \n"

    return err_msg


def get_err_msg_isin(signal: SignalNotIn) -> str:
    err_msg = f"parameter: {signal.parameter_name} \n" \
              f"\t violated : {signal.guarantee_type_name}.isin \n" \
              f"\t should   : {signal.isin} \n" \
              f"\t actual   : {signal.arg} \n"

    return err_msg


# TODO (snimu): put err_msg-creation into raise... -> only needs signal
def raise_type_warning_or_exception(
        err_msg: str,
        type_guarantee: TypeGuarantee
) -> None:
    if type_guarantee.warnings_only:
        warnings.warn(err_msg + "\t **Ignoring** \n")
    else:
        raise TypeError(err_msg)


def raise_value_warning_or_exception(
        err_msg: str,
        type_guarantee: TypeGuarantee
) -> None:
    if type_guarantee.warnings_only:
        warnings.warn(err_msg + "\t **Ignoring** \n")
    else:
        raise ValueError(err_msg)

