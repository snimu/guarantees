from typing import Union

from guarantees.functional_guarantees.classes import IsList, IsTuple, IsDict, \
    IsSet, IsFrozenSet, IsRange, TypeGuarantee, CollectionType
from guarantees.functional_guarantees.enforcement.util.typenames import \
    get_guaranteed_type, get_guaranteed_type_name, get_type_name, \
    get_guarantee_name
from guarantees.functional_guarantees.enforcement.util.error_handeling import \
    handle_error
from guarantees.functional_guarantees.enforcement.util.common_checks import \
    enforce_check_functions


def enforce_islist(arg: list, guarantee: IsList) -> list:
    arg = _check_type(arg, guarantee)
    _check_minmax_len(arg, guarantee)
    _check_contains(arg, guarantee)

    enforce_check_functions(arg, guarantee)
    return arg


def enforce_istuple(arg: tuple, guarantee: IsTuple) -> tuple:
    arg = _check_type(arg, guarantee)
    _check_minmax_len(arg, guarantee)
    _check_contains(arg, guarantee)

    enforce_check_functions(arg, guarantee)
    return arg


def enforce_isdict(arg: dict, guarantee: IsDict) -> dict:
    arg = _check_type(arg, guarantee)
    _check_minmax_len(arg, guarantee)
    _check_has_keys_values(arg, guarantee)

    enforce_check_functions(arg, guarantee)
    return arg


def enforce_isset(arg: set, guarantee: IsSet) -> set:
    arg = _check_type(arg, guarantee)
    _check_minmax_len(arg, guarantee)
    _check_contains(arg, guarantee)

    enforce_check_functions(arg, guarantee)
    return arg


def enforce_isfrozenset(arg: frozenset, guarantee: IsFrozenSet) -> frozenset:
    arg = _check_type(arg, guarantee)
    _check_minmax_len(arg, guarantee)
    _check_contains(arg, guarantee)

    enforce_check_functions(arg, guarantee)
    return arg


def enforce_isrange(arg: range, guarantee: IsRange) -> range:
    arg = _check_type(arg, guarantee)

    enforce_check_functions(arg, guarantee)
    return arg


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
        handle_error(
            where=guarantee.where,
            type_or_value="type",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "should_type": should_type_name,
                "actual_type": get_type_name(arg),
                "force_conversion": str(guarantee.force_conversion)
            }
        )

    return arg   # If handle_error only prints warning


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
        return False   # in case of warning instead of exception

    return True


def _max_len_is_legitimate(guarantee: CollectionType) -> bool:
    if guarantee.maximum_len is None:
        return False

    if type(guarantee.maximum_len) is not int:
        handle_error(
            where="internal",
            type_or_value="type",
            guarantee=guarantee,
            parameter_name=f"{get_guarantee_name(guarantee)}.maximum_len",
            what_dict={
                "should_type": "int",
                "actual_type": get_type_name(guarantee.minimum_len)
            }
        )
        return False   # in case of warning instead of exception

    return True


def _check_min_ge_max(guarantee: CollectionType) -> None:
    if not _min_len_is_legitimate(guarantee):
        return

    if not _max_len_is_legitimate(guarantee):
        return

    if guarantee.minimum_len >= guarantee.maximum_len:
        handle_error(
            where="internal",
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=f"{get_guarantee_name(guarantee)}.minimum_len & "
                           f"{get_guarantee_name(guarantee)}.maximum_len",
            what_dict={
                "error": f"minimum_len >= maximum_len ({guarantee.minimum_len} "
                         f"> {guarantee.maximum_len}"
            }
        )


def _check_min_len(
        arg: Union[list, tuple, dict, set, frozenset],
        guarantee: CollectionType
) -> None:
    if not _min_len_is_legitimate(guarantee):
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
                "should_len": guarantee.minimum_len,
                "actual_len": len(arg)
            }
        )


def _check_max_len(
        arg: Union[list, tuple, dict, set, frozenset],
        guarantee: CollectionType
) -> None:
    if not _max_len_is_legitimate(guarantee):
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
                "should_len": guarantee.maximum_len,
                "actual_len": len(arg)
            }
        )


def _check_contains(
        arg: Union[list, tuple, set, frozenset],
        guarantee: Union[IsList, IsTuple, IsSet, IsFrozenSet]
) -> None:
    if type(arg) is not get_guaranteed_type(guarantee):
        return

    if guarantee.contains is None:
        return

    missing = []

    for item in guarantee.contains:
        if item not in arg:
            missing.append(item)

    if len(missing) > 0:
        handle_error(
            where=guarantee.where,
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "error": f"violated "
                         f"{get_guarantee_name(guarantee)}.contains",
                "missing": missing
            }
        )


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

    missing = []
    for key in guarantee.has_keys:
        if key not in arg.keys():
            missing.append(key)

    if len(missing) > 0:
        handle_error(
            where=guarantee.where,
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "error": f"violated {get_guarantee_name(guarantee)}.has_keys",
                "missing": missing
            }
        )


def _check_has_values(arg: dict, guarantee: IsDict) -> None:
    if guarantee.has_values is None:
        return

    missing = []
    for val in guarantee.has_values:
        if val not in arg.values():
            missing.append(val)

    if len(missing) > 0:
        handle_error(
            where=guarantee.where,
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "error": f"violated {get_guarantee_name(guarantee)}.has_values",
                "missing": missing
            }
        )
