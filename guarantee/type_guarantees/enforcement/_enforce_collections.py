import warnings
from typing import Union

from guarantee.type_guarantees.guarantees import IsList, IsTuple, IsDict, \
    IsSet, IsFrozenSet, IsRange, TypeGuarantee, CollectionType
from guarantee.type_guarantees.signals.base import SignalTypeError
from guarantee.type_guarantees.signals.collections import \
    SignalMinLenGEMaxLen, SignalMinLenViolated, SignalMaxLenViolated, \
    SignalContainsViolated, SignalHasKeysViolated, SignalHasValuesViolated
from guarantee.type_guarantees.enforcement._util import \
    get_guaranteed_type, get_guaranteed_type_name, get_err_msg_type, \
    raise_warning_or_exception, get_type_name, get_guarantee_name, \
    get_err_msg_maximum_len_type, get_err_msg_minimum_len_type


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


def _check_type(
        arg: Union[list, tuple, dict, set, frozenset, range],
        guarantee: TypeGuarantee
) -> Union[list, tuple, dict, set, frozenset, range]:
    should_type = get_guaranteed_type(guarantee)
    should_type_name = get_guaranteed_type_name(guarantee)

    err = False
    if guarantee.force_conversion:
        try:
            arg = should_type(arg)
        except ValueError:
            err = True
    elif type(arg) is not should_type:
        err = True

    if err:
        type_signal = SignalTypeError(
            parameter_name=guarantee.parameter_name,
            should_type_name=should_type_name,
            is_type_name=get_type_name(arg),
            force_conversion=guarantee.force_conversion
        )
        if guarantee.callback is not None:
            guarantee.callback(type_signal)
        else:
            err_msg = get_err_msg_type(type_signal)
            raise_warning_or_exception(err_msg, guarantee)

    return arg


def _check_minmax_len(
        arg: Union[list, tuple, dict, set, frozenset],
        guarantee: CollectionType
) -> None:
    # if guarantee.warnings_only, this functon may be called even though
    #   the type-check failed --> check again and return if previous test failed
    if type(arg) is not get_guaranteed_type(guarantee):
        return

    _check_min_ge_max(guarantee)
    _check_min_len(arg, guarantee)
    _check_max_len(arg, guarantee)


def _min_len_is_legitimate(guarantee: CollectionType) -> bool:
    if guarantee.minimum_len is None:
        return False

    if type(guarantee.minimum_len) is not int:
        err_msg = get_err_msg_minimum_len_type(guarantee)
        raise_warning_or_exception(err_msg, guarantee)
        return False   # in case of warning instead of exception

    return True


def _max_len_is_legitimate(guarantee: CollectionType) -> bool:
    if guarantee.maximum_len is None:
        return False

    if type(guarantee.maximum_len) is not int:
        err_msg = get_err_msg_maximum_len_type(guarantee)
        raise_warning_or_exception(err_msg, guarantee)
        return False   # in case of warning instead of exception

    return True


# TODO (snimu) continue simplifying this with utils
def _check_min_ge_max(guarantee: CollectionType) -> None:
    if not _min_len_is_legitimate(guarantee):
        return

    if not _max_len_is_legitimate(guarantee):
        return

    if guarantee.minimum_len >= guarantee.maximum_len:
        arg_type = get_guaranteed_type_name(guarantee)
        if guarantee.callback is not None:
            guarantee.callback(
                SignalMinLenGEMaxLen(
                    parameter_name=guarantee.parameter_name,
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

    if len(arg) < guarantee.minimum_len:
        if guarantee.callback is not None:
            arg_type = get_guaranteed_type_name(guarantee)
            guarantee.callback(
                SignalMinLenViolated(
                    parameter_name=guarantee.parameter_name,
                    arg_type=arg_type,
                    arg=arg,
                    minimum_len=guarantee.minimum_len
                )
            )
        else:
            err_msg = f"Parameter {guarantee.parameter_name} had a guarantee for " \
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

    if len(arg) > guarantee.maximum_len:
        if guarantee.callback is not None:
            arg_type = get_guaranteed_type_name(guarantee)
            guarantee.callback(
                SignalMaxLenViolated(
                    parameter_name=guarantee.parameter_name,
                    arg_type=arg_type,
                    arg=arg,
                    maximum_len=guarantee.maximum_len
                )
            )
        else:
            err_msg = f"Parameter {guarantee.parameter_name} had a guarantee for " \
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
    if type(arg) is not get_guaranteed_type(guarantee):
        return

    if guarantee.contains is None:
        return

    for item in guarantee.contains:
        if item not in arg:
            arg_type_str = get_guaranteed_type_name(guarantee)
            if guarantee.callback is not None:
                guarantee.callback(
                    SignalContainsViolated(
                        parameter_name=guarantee.parameter_name,
                        arg_type=arg_type_str,
                        arg=arg,
                        contains=guarantee.contains
                    )
                )
            else:
                err_msg = f"You guaranteed that parameter {guarantee.parameter_name} " \
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
    if type(arg) is not get_guaranteed_type(guarantee):
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

    arg_type_str = get_guaranteed_type_name(guarantee)
    if kerr is not None:
        if guarantee.callback is not None:
            guarantee.callback(
                SignalHasKeysViolated(
                    parameter_name=guarantee.parameter_name,
                    arg_type=arg_type_str,
                    arg=arg,
                    has_keys=guarantee.has_values
                )
            )
        else:
            err_msg = f"Parameter {guarantee.parameter_name} of value {arg} " \
                      f"had a guarantee for " \
                      f"has_keys: {guarantee.has_keys}, but key " \
                      f"{kerr} is not contained in {guarantee.parameter_name}. "
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

    arg_type_str = get_guaranteed_type_name(guarantee)

    if verr is not None:
        if guarantee.callback is not None:
            guarantee.callback(
                SignalHasValuesViolated(
                    parameter_name=guarantee.parameter_name,
                    arg_type=arg_type_str,
                    arg=arg,
                    has_values=guarantee.has_values
                )
            )
        else:
            err_msg = f"Parameter {guarantee.parameter_name} of value {arg} " \
                      f"had a guarantee for " \
                      f"has_values: {guarantee.has_values}, but key " \
                      f"{verr} is not contained in {guarantee.parameter_name}. "
            if guarantee.warnings_only:
                warnings.warn(err_msg + "Ignoring.")
            else:
                raise ValueError(err_msg)
