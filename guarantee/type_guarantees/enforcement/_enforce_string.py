import warnings

from guarantee.type_guarantees.guarantees import IsStr
from guarantee.type_guarantees.signals.string \
    import SignalMaximumLenViolated, SignalMinimumLenViolated,\
    SignalMinimumLenGEMaximumLen, SignalNotIn
from guarantee.type_guarantees.signals.base import SignalTypeError


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

    if err:
        if guarantee.callback is not None:
            guarantee.callback(
                SignalTypeError(
                    arg_name=guarantee.name,
                    type_should="str",
                    type_is=str(type(arg)),
                    force_conversion=guarantee.force_conversion
                )
            )
        else:
            err_msg = f"Parameter {guarantee.name} is guaranteed to be " \
                      f"of type str but is of type {str(type(arg))}. "
            if guarantee.warnings_only:
                warnings.warn(err_msg + "Ignoring this parameter.")
            else:
                raise TypeError(err_msg)

    return arg


def _check_len(arg, guarantee: IsStr) -> None:
    if type(arg) is not str:   # Can happen if guarantee.warnings_only is True
        return

    _check_min_ge_max(guarantee)
    _check_min(arg, guarantee)
    _check_max(arg, guarantee)


def _check_min_ge_max(guarantee: IsStr) -> None:
    if guarantee.minimum_len is not None and guarantee.maximum_len is not None \
            and type(guarantee.minimum_len) is int \
            and type(guarantee.maximum_len) is int \
            and guarantee.minimum_len >= guarantee.maximum_len:
        if guarantee.callback is not None:
            guarantee.callback(
                SignalMinimumLenGEMaximumLen(
                    arg_name=guarantee.name,
                    arg_type="str",
                    minimum_len=guarantee.minimum_len,
                    maximum_len=guarantee.maximum_len
                )
            )
        else:
            err_msg = f"Parameter {guarantee.name} has " \
                      f"minimum_len {guarantee.minimum_len} and maximum_len " \
                      f"{guarantee.maximum_len} guaranteed; minimum_len " \
                      f"must be less than maximum_len!"
            if guarantee.warnings_only:
                warnings.warn(err_msg)
            else:
                raise ValueError(err_msg)


def _check_min(arg, guarantee: IsStr) -> None:
    if type(arg) is not str:
        return

    if guarantee.minimum_len is None:
        return

    if type(guarantee.minimum_len) is not int:
        err_msg = f"Type of minimum_len should be int but is " \
                  f"{type(guarantee.minimum_len)}. "

        if guarantee.warnings_only:
            warnings.warn(err_msg + "Ignoring.")
            return
        else:
            raise TypeError(err_msg)

    if len(arg) < guarantee.minimum_len:
        if guarantee.callback is not None:
            guarantee.callback(
                SignalMinimumLenViolated(
                    arg_name=guarantee.name,
                    arg=arg,
                    minimum_len=guarantee.minimum_len
                )
            )
        else:
            err_msg = f"Parameter {guarantee.name} violated guarantee " \
                      f"'minimum_len': {len(arg)} < {guarantee.minimum_len}. "

            if guarantee.warnings_only:
                warnings.warn(err_msg + "Ignoring.")
                return
            else:
                raise ValueError(err_msg)


def _check_max(arg, guarantee: IsStr) -> None:
    if type(arg) is not str:
        return

    if guarantee.maximum_len is None:
        return

    if type(guarantee.maximum_len) is not int:
        err_msg = f"Type of maximum_len should be int but is " \
                  f"{type(guarantee.maximum_len)}. "

        if guarantee.warnings_only:
            warnings.warn(err_msg + "Ignoring.")
            return
        else:
            raise TypeError(err_msg)

    if len(arg) > guarantee.maximum_len:
        if guarantee.callback is not None:
            guarantee.callback(
                SignalMaximumLenViolated(
                    arg_name=guarantee.name,
                    arg=arg,
                    maximum_len=guarantee.maximum_len
                )
            )
        else:
            err_msg = f"Parameter {guarantee.name} violated guarantee " \
                      f"'maximum_len': {len(arg)} > {guarantee.maximum_len}. "

            if guarantee.warnings_only:
                warnings.warn(err_msg + "Ignoring.")
                return
            else:
                raise ValueError(err_msg)


def _check_isin(arg: str, guarantee: IsStr) -> None:
    if type(arg) is not str:
        return

    if guarantee.isin is None:
        return

    if type(guarantee.isin) is not list:
        err_msg = "isin should be of type list but is of type " \
                  f"{type(guarantee.isin)}. "
        if guarantee.warnings_only:
            warnings.warn(err_msg + "Ignoring.")
            return
        else:
            raise TypeError(err_msg)

    if arg not in guarantee.isin:
        if guarantee.callback is not None:
            guarantee.callback(
                SignalNotIn(
                    arg_name=guarantee.name,
                    arg=arg,
                    isin=guarantee.isin
                )
            )
        else:
            err_msg = f"Parameter {guarantee.name} was guaranteed to be in " \
                      f"{guarantee.isin} but is not. "
            if guarantee.warnings_only:
                warnings.warn(err_msg + "Ignoring.")
            else:
                raise ValueError(err_msg)
