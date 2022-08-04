import warnings
from typing import Union

from guarantee.type_guarantees.guarantees import IsList, IsTuple, IsDict, \
    IsSet, IsFrozenSet, IsRange, TypeGuarantee, CollectionType
from guarantee.type_guarantees.signals.base import SignalTypeError
from guarantee.type_guarantees.signals.collections import \
    SignalMinLenGEMaxLen, SignalMinLenViolated, SignalMaxLenViolated, \
    SignalContainsViolated, SignalHasKeysViolated, SignalHasValuesViolated


def enforce_islist(arg: list, guarantee: IsList) -> list:
    arg = _check_type(arg, guarantee)
    _check_minmax_len(arg, guarantee)
    _check_contains(arg, guarantee)
    return arg


def enforce_istuple(arg: tuple, guarantee: IsTuple) -> tuple:
    arg = _check_type(arg, guarantee)
    _check_minmax_len(arg, guarantee)
    _check_contains(arg, guarantee)
    return arg


def enforce_isdict(arg: dict, guarantee: IsDict) -> dict:
    arg = _check_type(arg, guarantee)
    _check_minmax_len(arg, guarantee)
    _check_has_keys_values(arg, guarantee)
    return arg


def enforce_isset(arg: set, guarantee: IsSet) -> set:
    arg = _check_type(arg, guarantee)
    _check_minmax_len(arg, guarantee)
    _check_contains(arg, guarantee)
    return arg


def enforce_isfrozenset(arg: frozenset, guarantee: IsFrozenSet) -> frozenset:
    arg = _check_type(arg, guarantee)
    _check_minmax_len(arg, guarantee)
    _check_contains(arg, guarantee)
    return arg


def enforce_isrange(arg: range, guarantee: IsRange) -> range:
    return _check_type(arg, guarantee)


guarantee_type_dict = {
    IsList: list,
    IsTuple: tuple,
    IsDict: dict,
    IsSet: set,
    IsFrozenSet: frozenset,
    IsRange: range
}

guarantee_type_name_dict = {
    IsList: "list",
    IsTuple: "tuple",
    IsDict: "dict",
    IsSet: "set",
    IsFrozenSet: "frozenset",
    IsRange: "range"
}


def _check_type(
        arg: Union[list, tuple, dict, set, frozenset, range],
        guarantee: TypeGuarantee
) -> Union[list, tuple, dict, set, frozenset, range]:
    global guarantee_type_dict
    global guarantee_type_name_dict

    type_should = guarantee_type_dict[type(guarantee)]
    type_should_str = guarantee_type_name_dict[type(guarantee)]

    err = False
    if guarantee.force_conversion:
        try:
            arg = type_should(arg)
        except ValueError:
            err = True
    elif type(arg) is not type_should:
        err = True

    if err:
        if guarantee.callback is not None:
            guarantee.callback(
                SignalTypeError(
                    arg_name=guarantee.name,
                    type_should=type_should_str,
                    type_is=type(arg),
                    force_conversion=guarantee.force_conversion
                )
            )
        else:
            err_msg = f"Guaranteed type {type_should_str} " \
                      f"for parameter {guarantee.name}, " \
                      f"but received type {str(type(arg))}. " \
                      f"Called with " \
                      f"force_conversion={guarantee.force_conversion}. "
            if guarantee.warnings_only:
                warnings.warn(err_msg + "Ignoring")
            else:
                raise TypeError(err_msg)

    return arg


def _check_minmax_len(
        arg: Union[list, tuple, dict, set, frozenset],
        guarantee: CollectionType
) -> None:
    # if guarantee.warnings_only, this functon may be called even though
    #   the type-check failed --> check again and return if previous test failed
    global guarantee_type_dict
    if type(arg) is not guarantee_type_dict[type(guarantee)]:
        return

    _check_min_ge_max(guarantee)
    _check_min_len(arg, guarantee)
    _check_max_len(arg, guarantee)


def _min_len_is_legitimate(guarantee: CollectionType) -> bool:
    if guarantee.minimum_len is None:
        return False

    if type(guarantee.minimum_len) is not int:
        err_msg = "You guaranteed minimum_len, but made it of type " \
                  f"{str(type(guarantee.minimum_len))}. It must be None or " \
                  f"of type int. "
        if guarantee.warnings_only:
            warnings.warn(err_msg + "Ignoring")
            return False
        else:
            raise TypeError(err_msg)

    return True


def _max_len_is_legitimate(guarantee: CollectionType) -> bool:
    if guarantee.maximum_len is None:
        return False

    if type(guarantee.maximum_len) is not int:
        err_msg = "You guaranteed maximum_len, but made it of type " \
                  f"{str(type(guarantee.maximum_len))}. It must be None or " \
                  f"of type int. "
        if guarantee.warnings_only:
            warnings.warn(err_msg + "Ignoring")
            return False
        else:
            raise TypeError(err_msg)

    return True


def _check_min_ge_max(guarantee: CollectionType) -> None:
    if not _min_len_is_legitimate(guarantee):
        return

    if not _max_len_is_legitimate(guarantee):
        return

    if guarantee.minimum_len >= guarantee.maximum_len:
        global guarantee_type_name_dict
        arg_type = guarantee_type_name_dict[type(guarantee)]
        if guarantee.callback is not None:
            guarantee.callback(
                SignalMinLenGEMaxLen(
                    arg_name=guarantee.name,
                    arg_type=arg_type,
                    minimum_len=guarantee.minimum_len,
                    maximum_len=guarantee.maximum_len
                )
            )
        else:
            err_msg = f"You guaranteed minimum_len and maximum_len, but " \
                      f"minimum_len >= maximum_len: {guarantee.minimum_len} " \
                      f">= {guarantee.maximum_len}. "
            if guarantee.warnings_only:
                warnings.warn(err_msg + "Ignoring.")
            else:
                raise ValueError(err_msg)


def _check_min_len(
        arg: Union[list, tuple, dict, set, frozenset],
        guarantee: CollectionType
) -> None:
    if not _min_len_is_legitimate(guarantee):
        return

    global guarantee_type_dict
    if type(arg) is not guarantee_type_dict[type(guarantee)]:
        return

    if len(arg) < guarantee.minimum_len:
        if guarantee.callback is not None:
            global guarantee_type_name_dict
            arg_type = guarantee_type_name_dict[type(guarantee)]
            guarantee.callback(
                SignalMinLenViolated(
                    arg_name=guarantee.name,
                    arg_type=arg_type,
                    arg=arg,
                    minimum_len=guarantee.minimum_len
                )
            )
        else:
            err_msg = f"Parameter {guarantee.name} had a guarantee for " \
                      f"minimum_len of {guarantee.minimum_len}, but has " \
                      f"length {len(arg)}. "
            if guarantee.warnings_only:
                warnings.warn(err_msg + "Ignoring.")
            else:
                raise ValueError(err_msg)


def _check_max_len(
        arg: Union[list, tuple, dict, set, frozenset],
        guarantee: CollectionType
) -> None:
    if not _max_len_is_legitimate(guarantee):
        return

    global guarantee_type_dict
    if type(arg) is not guarantee_type_dict[type(guarantee)]:
        return

    if len(arg) > guarantee.maximum_len:
        if guarantee.callback is not None:
            global guarantee_type_name_dict
            arg_type = guarantee_type_name_dict[type(guarantee)]
            guarantee.callback(
                SignalMaxLenViolated(
                    arg_name=guarantee.name,
                    arg_type=arg_type,
                    arg=arg,
                    maximum_len=guarantee.maximum_len
                )
            )
        else:
            err_msg = f"Parameter {guarantee.name} had a guarantee for " \
                      f"maximum_len of {guarantee.maximum_len}, but has " \
                      f"length {len(arg)}. "
            if guarantee.warnings_only:
                warnings.warn(err_msg + "Ignoring.")
            else:
                raise ValueError(err_msg)


def _check_contains(
        arg: Union[list, tuple, set, frozenset],
        guarantee: Union[IsList, IsTuple, IsSet, IsFrozenSet]
) -> None:
    global guarantee_type_dict
    if type(arg) is not guarantee_type_dict[type(guarantee)]:
        return

    if guarantee.contains is None:
        return

    for item in guarantee.contains:
        if item not in arg:
            global guarantee_type_name_dict
            arg_type_str = guarantee_type_name_dict[type(guarantee)]
            if guarantee.callback is not None:
                guarantee.callback(
                    SignalContainsViolated(
                        arg_name=guarantee.name,
                        arg_type=arg_type_str,
                        arg=arg,
                        contains=guarantee.contains
                    )
                )
            else:
                err_msg = f"You guaranteed that parameter {guarantee.name} " \
                          f"contains one of the following items: " \
                          f"{guarantee.contains}. However, " \
                          f"at least item {item} is missing from parameter " \
                          f"with value {arg}. "
                if guarantee.warnings_only:
                    warnings.warn(err_msg + "Ignoring")
                else:
                    raise ValueError(err_msg)


def _check_has_keys_values(
        arg: dict,
        guarantee: IsDict
) -> None:
    global guarantee_type_dict
    if type(arg) is not guarantee_type_dict[type(guarantee)]:
        return

    _check_has_keys(arg, guarantee)
    _check_has_values(arg, guarantee)


def _check_has_keys(arg: dict, guarantee: IsDict) -> None:
    if guarantee.has_keys is None:
        return

    kerr = None

    for key in guarantee.has_keys:
        if key not in arg.keys():
            kerr = key
            break

    global guarantee_type_name_dict
    arg_type_str = guarantee_type_name_dict[type(guarantee)]
    if kerr is not None:
        if guarantee.callback is not None:
            guarantee.callback(
                SignalHasKeysViolated(
                    arg_name=guarantee.name,
                    arg_type=arg_type_str,
                    arg=arg,
                    has_keys=guarantee.has_values
                )
            )
        else:
            err_msg = f"Parameter {guarantee.name} of value {arg} " \
                      f"had a guarantee for " \
                      f"has_keys: {guarantee.has_keys}, but key " \
                      f"{kerr} is not contained in {guarantee.name}. "
            if guarantee.warnings_only:
                warnings.warn(err_msg + "Ignoring.")
            else:
                raise ValueError(err_msg)


def _check_has_values(arg: dict, guarantee: IsDict) -> None:
    if guarantee.has_values is None:
        return

    verr = None

    for val in guarantee.has_values:
        if val not in arg.values():
            verr = val
            break

    global guarantee_type_name_dict
    arg_type_str = guarantee_type_name_dict[type(guarantee)]

    if verr is not None:
        if guarantee.callback is not None:
            guarantee.callback(
                SignalHasValuesViolated(
                    arg_name=guarantee.name,
                    arg_type=arg_type_str,
                    arg=arg,
                    has_values=guarantee.has_values
                )
            )
        else:
            err_msg = f"Parameter {guarantee.name} of value {arg} " \
                      f"had a guarantee for " \
                      f"has_values: {guarantee.has_values}, but key " \
                      f"{verr} is not contained in {guarantee.name}. "
            if guarantee.warnings_only:
                warnings.warn(err_msg + "Ignoring.")
            else:
                raise ValueError(err_msg)
