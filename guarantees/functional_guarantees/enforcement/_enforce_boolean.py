from guarantees.functional_guarantees.classes import IsBool
from guarantees.functional_guarantees.enforcement.util.typenames import \
    get_type_name, get_guaranteed_type_name
from guarantees.functional_guarantees.enforcement.util.error_handeling import \
    handle_error


def enforce_isbool(arg: bool, guarantee: IsBool) -> bool:
    arg = _check_type(arg, guarantee)

    if guarantee.check_function is not None:
        arg = guarantee.check_function(arg)
    return arg


def _check_type(arg: bool, guarantee: IsBool) -> bool:
    err = False

    if guarantee.force_conversion:
        try:
            arg = bool(arg)
        except ValueError:
            err = True
    else:
        if type(arg) is not bool:
            err = True

    if not err:
        return arg

    handle_error(
        where=guarantee.where,
        type_or_value="type",
        guarantee=guarantee,
        parameter_name=guarantee.parameter_name,
        what_dict={
            "should_type": get_guaranteed_type_name(guarantee),
            "actual_type": get_type_name(arg)
        }
    )
