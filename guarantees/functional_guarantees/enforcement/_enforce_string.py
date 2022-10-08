from guarantees.functional_guarantees.classes import IsStr
from guarantees.functional_guarantees.enforcement._util import \
    get_guarantee_name, get_type_name, handle_error


def enforce_isstr(arg: str, guarantee: IsStr) -> str:
    arg = _check_type(arg, guarantee)
    _check_len(arg, guarantee)
    _check_isin(arg, guarantee)

    if guarantee.check_function is not None:
        arg = guarantee.check_function(arg)
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
        handle_error(
            where=guarantee.where,
            type_or_value="type",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "should_type": "str",
                "actual_type": get_type_name(arg)
            }
        )

    return arg


def _check_len(arg, guarantee: IsStr) -> None:
    if type(arg) is not str:   # Can happen if guarantees.warnings_only is True
        return

    _check_min_len_ge_max_len(guarantee)
    _check_min_len(arg, guarantee)
    _check_max_len(arg, guarantee)


def _minimum_len_type_is_correct(guarantee: IsStr) -> bool:
    if type(guarantee.minimum_len) is int:
        return True

    handle_error(
        where="internal",
        type_or_value="type",
        guarantee=guarantee,
        parameter_name=f"{get_guarantee_name(guarantee)}.minimum_len",
        what_dict={
            "should_type": "int",
            "actual_type": get_type_name(guarantee.minimum_len)
        }
    )

    return False   # in case of warnings_only


def _maximum_len_type_is_correct(guarantee: IsStr) -> bool:
    if type(guarantee.maximum_len) is int:
        return True

    handle_error(
        where="internal",
        type_or_value="type",
        guarantee=guarantee,
        parameter_name=f"{get_guarantee_name(guarantee)}.maximum_len",
        what_dict={
            "should_type": "int",
            "actual_type": get_type_name(guarantee.maximum_len)
        }
    )

    return False   # in case of warnings_only


def _check_min_len_ge_max_len(guarantee: IsStr) -> None:
    if guarantee.minimum_len is None or guarantee.maximum_len is None:
        return

    if not _minimum_len_type_is_correct(guarantee) \
            or not _maximum_len_type_is_correct(guarantee):
        return

    if guarantee.minimum_len >= guarantee.maximum_len:
        handle_error(
            where="internal",
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=f"{get_guarantee_name(guarantee)}.minimum_len "
                           f"and {get_guarantee_name(guarantee)}.maximum_len",
            what_dict={
                "error": "minimum_len >= maximum_len",
                "minimum_len": str(guarantee.minimum_len),
                "maximum_len": str(guarantee.maximum_len)
            }
        )


def _check_min_len(arg, guarantee: IsStr) -> None:
    if type(arg) is not str:
        return

    if guarantee.minimum_len is None:
        return

    if not _minimum_len_type_is_correct(guarantee):
        return

    if len(arg) < guarantee.minimum_len:
        handle_error(
            where=guarantee.where,
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "error": f"violated "
                         f"{get_guarantee_name(guarantee)}.minimum_len",
                "minimum_len": str(guarantee.minimum_len),
                "actual len": str(len(arg))
            }
        )


def _check_max_len(arg, guarantee: IsStr) -> None:
    if type(arg) is not str:
        return

    if guarantee.maximum_len is None:
        return

    if not _maximum_len_type_is_correct(guarantee):
        return

    if len(arg) > guarantee.maximum_len:
        handle_error(
            where=guarantee.where,
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "error": f"violated "
                         f"{get_guarantee_name(guarantee)}.maximum_len",
                "maximum_len": str(guarantee.maximum_len),
                "actual len": str(len(arg))
            }
        )


def _check_isin(arg: str, guarantee: IsStr) -> None:
    if type(arg) is not str:
        return

    if guarantee.isin is None:
        return

    if type(guarantee.isin) is not list:
        handle_error(
            where="internal",
            type_or_value="type",
            guarantee=guarantee,
            parameter_name=f"{get_guarantee_name(guarantee)}.isin",
            what_dict={
                "should_type": "list",
                "actual_type": get_type_name(guarantee.isin)
            }
        )

    if arg in guarantee.isin:
        return

    handle_error(
        where=guarantee.where,
        type_or_value="value",
        guarantee=guarantee,
        parameter_name=guarantee.parameter_name,
        what_dict={
            "error": f"violated {get_guarantee_name(guarantee)}.isin",
            "isin": f"{guarantee.isin}",
            "actual": arg  # is str
        }
    )
