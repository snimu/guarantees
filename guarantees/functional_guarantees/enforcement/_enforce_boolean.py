from guarantees.functional_guarantees.classes import IsBool
from guarantees.functional_guarantees.enforcement._util import \
    get_type_name, get_guaranteed_type_name, raise_warning_or_exception, \
    choose_exception


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

    exception = choose_exception(where=guarantee.where, what="type")
    exception = exception(
        function_name=guarantee.function_name,
        function_namespace=guarantee.function_namespace,
        guarantee_type_name=get_guaranteed_type_name(guarantee),
        what_dict={
            "should_type_name": get_guaranteed_type_name(guarantee),
            "actual_type_name": get_type_name(arg)
        }
    )

    if guarantee.error_callback is not None:
        guarantee.error_callback(exception)
    else:
        raise_warning_or_exception(exception, guarantee)
