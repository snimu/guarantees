import warnings
from typing import Union

from guarantees.parameter_guarantees.classes import IsList, IsTuple, IsDict, \
    IsSet, IsFrozenSet, IsRange, TypeGuarantee, CollectionType
from guarantees.parameter_guarantees.signals.base import SignalTypeError
from guarantees.parameter_guarantees.signals.collections import \
    SignalMinLenGEMaxLen, SignalMinLenViolated, SignalMaxLenViolated, \
    SignalContainsViolated, SignalHasKeysViolated, SignalHasValuesViolated
from guarantees.parameter_guarantees.enforcement._util import \
    get_guaranteed_type, get_guaranteed_type_name, get_err_msg_type, \
    raise_type_warning_or_exception, get_type_name, get_guarantee_name, \
    get_err_msg_maximum_len_type, get_err_msg_minimum_len_type, \
    get_err_msg_minimum_ge_maximum, raise_value_warning_or_exception, \
    get_err_msg_minimum_len, get_err_msg_maximum_len


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
            raise_type_warning_or_exception(err_msg, guarantee)

    return arg


def _check_minmax_len(
        arg: Union[list, tuple, dict, set, frozenset],
        guarantee: CollectionType
) -> None:
    # if guarantees.warnings_only, this functon may be called even though
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
        raise_type_warning_or_exception(err_msg, guarantee)
        return False   # in case of warning instead of exception

    return True


def _max_len_is_legitimate(guarantee: CollectionType) -> bool:
    if guarantee.maximum_len is None:
        return False

    if type(guarantee.maximum_len) is not int:
        err_msg = get_err_msg_maximum_len_type(guarantee)
        raise_type_warning_or_exception(err_msg, guarantee)
        return False   # in case of warning instead of exception

    return True


def _check_min_ge_max(guarantee: CollectionType) -> None:
    if not _min_len_is_legitimate(guarantee):
        return

    if not _max_len_is_legitimate(guarantee):
        return

    if guarantee.minimum_len >= guarantee.maximum_len:
        signal_minlen_ge_maxlen = SignalMinLenGEMaxLen(
            parameter_name=guarantee.parameter_name,
            arg_type=get_guaranteed_type_name(guarantee),
            minimum_len=guarantee.minimum_len,
            maximum_len=guarantee.maximum_len
        )
        if guarantee.callback is not None:
            guarantee.callback(signal_minlen_ge_maxlen)
        else:
            err_msg = get_err_msg_minimum_ge_maximum(
                guarantee, guarantee.minimum_len, guarantee.maximum_len)
            raise_value_warning_or_exception(err_msg)


def _check_min_len(
        arg: Union[list, tuple, dict, set, frozenset],
        guarantee: CollectionType
) -> None:
    if not _min_len_is_legitimate(guarantee):
        return

    if len(arg) < guarantee.minimum_len:
        signal_min = SignalMinLenViolated(
            parameter_name=guarantee.parameter_name,
            arg_type=get_guaranteed_type_name(guarantee),
            arg=arg,
            minimum_len=guarantee.minimum_len
        )
        if guarantee.callback is not None:
            guarantee.callback(signal_min)
        else:
            err_msg = get_err_msg_minimum_len(guarantee, guarantee.minimum_len,
                                              len(arg))
            raise_value_warning_or_exception(err_msg, guarantee)


def _check_max_len(
        arg: Union[list, tuple, dict, set, frozenset],
        guarantee: CollectionType
) -> None:
    if not _max_len_is_legitimate(guarantee):
        return

    if len(arg) > guarantee.maximum_len:
        signal_max = SignalMaxLenViolated(
            parameter_name=guarantee.parameter_name,
            arg_type=get_guaranteed_type_name(guarantee),
            arg=arg,
            maximum_len=guarantee.maximum_len
        )
        if guarantee.callback is not None:
            guarantee.callback(signal_max)
        else:
            err_msg = get_err_msg_maximum_len(guarantee, guarantee.maximum_len,
                                              len(arg))
            raise_value_warning_or_exception(err_msg, guarantee)


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
