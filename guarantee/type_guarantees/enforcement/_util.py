import warnings

import guarantee


guarantee_to_type_dict = {
    guarantee.IsInt: int,
    guarantee.IsFloat: float,
    guarantee.IsComplex: complex,
    guarantee.IsBool: bool,
    guarantee.IsStr: str,
    guarantee.IsList: list,
    guarantee.IsTuple: tuple,
    guarantee.IsDict: dict,
    guarantee.IsSet: set,
    guarantee.IsFrozenSet: frozenset,
    guarantee.IsRange: range,
    guarantee.IsClass: object,
    guarantee.IsBytes: bytes,
    guarantee.IsByteArray: bytearray,
    guarantee.IsMemoryView: memoryview
}


guarantee_to_type_name_dict = {
    guarantee.IsInt: "int",
    guarantee.IsFloat: "float",
    guarantee.IsComplex: "complex",
    guarantee.IsBool: "bool",
    guarantee.IsStr: "str",
    guarantee.IsList: "list",
    guarantee.IsTuple: "tuple",
    guarantee.IsDict: "dict",
    guarantee.IsSet: "set",
    guarantee.IsFrozenSet: "frozenset",
    guarantee.IsRange: "range",
    guarantee.IsClass: "object",
    guarantee.IsBytes: "bytes",
    guarantee.IsByteArray: "bytearray",
    guarantee.IsMemoryView: "memoryview"
}


def get_guaranteed_type(type_guarantee: guarantee.TypeGuarantee):
    global guarantee_to_type_dict
    return guarantee_to_type_dict[type(type_guarantee)]


def get_guaranteed_type_name(type_guarantee: guarantee.TypeGuarantee):
    global guarantee_to_type_name_dict
    return guarantee_to_type_name_dict[type(type_guarantee)]


def get_type_err_msg(signal: guarantee.signals.base.SignalTypeError) -> str:
    err_str = f"parameter: {signal.parameter_name} \n" \
              f"\t guarantee: type \n" \
              f"\t type should: {signal.should_type_name} \n" \
              f"\t type is:     {signal.is_type_name} \n" \
              f"\t force_conversion: {signal.force_conversion} \n"

    return err_str


def type_warning_or_exception(
        err_msg: str,
        type_guarantee: guarantee.TypeGuarantee
) -> None:
    if type_guarantee.warnings_only:
        warnings.warn(err_msg + " \n\t **Ignoring**")
    else:
        raise TypeError(err_msg)

