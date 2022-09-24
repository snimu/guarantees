from guarantees.parameter_guarantees.classes import IsStr
from guarantees.parameter_guarantees.signals.common import SignalTypeError, \
    SignalMinLenGEMaxLen, SignalMinLenViolated, SignalMaxLenViolated, \
    SignalNotIn
from guarantees.parameter_guarantees.enforcement._util import \
    raise_type_warning_or_exception, raise_value_warning_or_exception, \
    get_guarantee_name, get_type_name, \
    get_err_msg_type, get_err_msg_minimum_len_type, \
    get_err_msg_maximum_len_type, get_err_msg_minimum_len_ge_maximum_len, \
    get_err_msg_minimum_len, get_err_msg_maximum_len, get_err_msg_isin


def enforce_isstr(arg: str, guarantee: IsStr) -> str:
    arg = _check_type(arg, guarantee)
    _check_len(arg, guarantee)
    _check_isin(arg, guarantee)
    return arg


def _check_type(arg: str, guarantee: IsStr) -> str:
    err = False

    if guarantee.force_conversion:
        try:
            arg = str(arg)
        except ValueError:
            err = True
    else:
        if not isinstance(arg, str):
            err = True

    if not err:
        return arg

    signal = SignalTypeError(
        parameter_name=guarantee.parameter_name,
        guarantee_type_name=get_guarantee_name(guarantee),
        should_type_name="str",
        is_type_name=get_type_name(arg)
    )
    if guarantee.error_callback is not None:
        guarantee.error_callback(signal)
    else:
        err_msg = get_err_msg_type(signal)
        raise_type_warning_or_exception(err_msg, guarantee)


def _check_len(arg, guarantee: IsStr) -> None:
    if type(arg) is not str:   # Can happen if guarantees.warnings_only is True
        return

    _check_min_len_ge_max_len(guarantee)
    _check_min_len(arg, guarantee)
    _check_max_len(arg, guarantee)


def _minimum_len_type_is_correct(guarantee: IsStr) -> bool:
    if type(guarantee.minimum_len) is int:
        return True

    signal = SignalTypeError(
        parameter_name=guarantee.parameter_name,
        guarantee_type_name=get_guarantee_name(guarantee),
        should_type_name="int",
        is_type_name=get_type_name(guarantee.minimum_len)
    )
    err_msg = get_err_msg_minimum_len_type(signal)
    raise_type_warning_or_exception(err_msg, guarantee)

    return False   # in case of warnings_only


def _maximum_len_type_is_correct(guarantee: IsStr) -> bool:
    if type(guarantee.maximum_len) is int:
        return True

    signal = SignalTypeError(
        parameter_name=guarantee.parameter_name,
        guarantee_type_name=get_guarantee_name(guarantee),
        should_type_name="int",
        is_type_name=get_type_name(guarantee.maximum_len)
    )
    err_msg = get_err_msg_maximum_len_type(signal)
    raise_type_warning_or_exception(err_msg, guarantee)

    return False   # in case of warnings_only


def _check_min_len_ge_max_len(guarantee: IsStr) -> None:
    if guarantee.minimum_len is None or guarantee.maximum_len is None:
        return

    if not _minimum_len_type_is_correct(guarantee) \
            or not _maximum_len_type_is_correct(guarantee):
        return

    if guarantee.minimum_len >= guarantee.maximum_len:
        signal = SignalMinLenGEMaxLen(
            parameter_name=guarantee.parameter_name,
            guarantee_type_name=get_guarantee_name(guarantee),
            minimum_len=guarantee.minimum_len,
            maximum_len=guarantee.maximum_len
        )
        if guarantee.error_callback is not None:
            guarantee.error_callback(signal)
        else:
            err_msg = get_err_msg_minimum_len_ge_maximum_len(signal)
            raise_value_warning_or_exception(err_msg, guarantee)


def _check_min_len(arg, guarantee: IsStr) -> None:
    if type(arg) is not str:
        return

    if guarantee.minimum_len is None:
        return

    if not _minimum_len_type_is_correct(guarantee):
        return

    if len(arg) < guarantee.minimum_len:
        signal = SignalMinLenViolated(
            parameter_name=guarantee.parameter_name,
            guarantee_type_name=get_guarantee_name(guarantee),
            minimum_len=guarantee.minimum_len,
            arg=arg
        )
        if guarantee.error_callback is not None:
            guarantee.error_callback(signal)
        else:
            err_msg = get_err_msg_minimum_len(signal)
            raise_value_warning_or_exception(err_msg, guarantee)


def _check_max_len(arg, guarantee: IsStr) -> None:
    if type(arg) is not str:
        return

    if guarantee.maximum_len is None:
        return

    if not _maximum_len_type_is_correct(guarantee):
        return

    if len(arg) > guarantee.maximum_len:
        signal = SignalMaxLenViolated(
            parameter_name=guarantee.parameter_name,
            guarantee_type_name=get_guarantee_name(guarantee),
            maximum_len=guarantee.maximum_len,
            arg=arg
        )
        if guarantee.error_callback is not None:
            guarantee.error_callback(signal)
        else:
            err_msg = get_err_msg_maximum_len(signal)
            raise_value_warning_or_exception(err_msg, guarantee)


def _check_isin(arg: str, guarantee: IsStr) -> None:
    if type(arg) is not str:
        return

    if guarantee.isin is None:
        return

    if type(guarantee.isin) is not list:
        err_msg = f"parameter: {guarantee.parameter_name} \n" \
                  f"\t violated: type -- guarantee \n" \
                  f"\t should: list \n" \
                  f"\t actual: {get_type_name(guarantee.isin)} \n"
        raise_type_warning_or_exception(err_msg, guarantee)

    if arg in guarantee.isin:
        return

    signal = SignalNotIn(
        parameter_name=guarantee.parameter_name,
        guarantee_type_name=get_guarantee_name(guarantee),
        isin=guarantee.isin,
        arg=arg
    )
    if guarantee.error_callback is not None:
        guarantee.error_callback(signal)
    else:
        err_msg = get_err_msg_isin(signal)
        raise_value_warning_or_exception(err_msg, guarantee)
