from typing import Union

from guarantees.functional_guarantees.classes import IsInt, IsFloat, IsComplex, \
    NumericGuarantee
from guarantees.functional_guarantees.enforcement.util.typenames import \
    get_guaranteed_type, get_guaranteed_type_name, get_guarantee_name, \
    get_type_name
from guarantees.functional_guarantees.enforcement.util.error_handeling import \
    handle_error
from guarantees.functional_guarantees.enforcement.util.common_checks import \
    enforce_check_functions


def enforce_isint(arg: int, guarantee: IsInt) -> int:
    arg = _check_type(arg, guarantee)

    _check_min_ge_max(
        guarantee=guarantee,
        minimum=guarantee.minimum,
        maximum=guarantee.maximum
    )

    _check_min(arg, guarantee.minimum, guarantee, "int")
    _check_max(arg, guarantee.maximum, guarantee, "int")

    _check_isin(arg, guarantee)

    enforce_check_functions(arg, guarantee)

    return arg


def enforce_isfloat(arg: float, guarantee: IsFloat) -> float:
    arg = _check_type(arg, guarantee)

    _check_min_ge_max(
        guarantee=guarantee,
        minimum=guarantee.minimum,
        maximum=guarantee.maximum
    )

    _check_min(arg, guarantee.minimum, guarantee)
    _check_max(arg, guarantee.maximum, guarantee)

    _check_isin(arg, guarantee)

    enforce_check_functions(arg, guarantee)

    return arg


def enforce_iscomplex(arg: complex, guarantee: IsComplex) -> complex:
    arg = _check_type(arg, guarantee)

    _check_min_ge_max(
        guarantee=guarantee,
        minimum=guarantee.minimum,
        maximum=guarantee.maximum
    )
    _check_min_ge_max(
        guarantee=guarantee,
        minimum=guarantee.minimum_re,
        maximum=guarantee.maximum_re,
        minmax_type="re"
    )
    _check_min_ge_max(
        guarantee=guarantee,
        minimum=guarantee.minimum_im,
        maximum=guarantee.maximum_im,
        minmax_type="im"
    )

    _check_min(abs(arg), guarantee.minimum, guarantee)
    _check_max(abs(arg), guarantee.maximum, guarantee)
    _check_min(arg.real, guarantee.minimum_re, guarantee, "re")
    _check_max(arg.real, guarantee.maximum_re, guarantee, "re")
    _check_min(arg.imag, guarantee.minimum_im, guarantee, "im")
    _check_max(arg.imag, guarantee.maximum_im, guarantee, "im")

    _check_isin(arg, guarantee)

    enforce_check_functions(arg, guarantee)

    return arg


def _check_type(
        arg: Union[int, float, complex],
        guarantee: NumericGuarantee
) -> Union[int, float, complex]:
    type_should_str = get_guaranteed_type_name(guarantee)
    type_should = get_guaranteed_type(guarantee)
    type_is_str = get_type_name(arg)

    # Do tests
    err = False

    if guarantee.force_conversion:
        try:
            arg = type_should(arg)
        except ValueError:
            err = True
    else:
        if type(arg) is not type_should:
            err = True

    if err:
        handle_error(
            where=guarantee.where,
            type_or_value="type",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "should_type": type_should_str,
                "actual_type": type_is_str
            }
        )

    return arg  # if warnings_only


def _check_minimum_type(
        minimum: Union[int, float],
        guarantee: NumericGuarantee
) -> None:
    if type(minimum) not in [int, float]:
        handle_error(
            where="internal",
            type_or_value="type",
            guarantee=guarantee,
            parameter_name=f"{get_guarantee_name(guarantee)}.minimum",
            what_dict={
                "should_type": \
                    "int" if isinstance(guarantee, IsInt) else "float",
                "actual_type": get_type_name(minimum)
            }
        )


def _check_maximum_type(
        maximum: Union[int, float],
        guarantee: NumericGuarantee
) -> None:
    if type(maximum) not in [int, float]:
        handle_error(
            where="internal",
            type_or_value="type",
            guarantee=guarantee,
            parameter_name=f"{get_guarantee_name(guarantee)}.maximum",
            what_dict={
                "should_type": \
                    "int" if isinstance(guarantee, IsInt) else "float",
                "actual_type": get_type_name(maximum)
            }
        )


def _check_min_ge_max(
        guarantee: NumericGuarantee,
        minimum: Union[int, float, complex],
        maximum: Union[int, float, complex],
        minmax_type: str = "abs"
) -> None:
    if minimum is not None and maximum is not None and minimum >= maximum:
        _check_minimum_type(minimum, guarantee)
        _check_maximum_type(maximum, guarantee)

        minimum_name = "minimum" if minmax_type == "abs" else "minimum_" + minmax_type
        maximum_name = "maximum" if minmax_type == "abs" else "minimum_" + minmax_type

        handle_error(
            where="internal",
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=f"{get_guarantee_name(guarantee)}.{minimum_name} "
                           f"and {get_type_name(guarantee)}.{maximum_name}",
            what_dict={
                "error": f"{minimum_name} >= {maximum_name} ",
                "minimum": str(minimum),
                "maximum": str(maximum)
            }
        )


def _check_min(
        arg: Union[int, float, complex],
        minimum: Union[int, float, complex],
        guarantee: NumericGuarantee,
        min_type: str = "abs"
) -> None:
    if minimum is None:
        return

    _check_minimum_type(minimum, guarantee)

    if arg < minimum:
        minimum_name = "minimum" if min_type == "abs" else "minimum_" + min_type
        handle_error(
            where=guarantee.where,
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "error": f"violated "
                         f"{get_guarantee_name(guarantee)}.{minimum_name}",
                "minimum": minimum,
                "actual": arg
            }
        )


def _check_max(
        arg: Union[int, float, complex],
        maximum: Union[int, float, complex],
        guarantee: NumericGuarantee,
        max_type: str = "abs"
) -> None:
    if maximum is None:
        return

    _check_maximum_type(maximum, guarantee)

    if arg > maximum:
        maximum_name = "maximum" if max_type == "abs" else "maximum_" + max_type
        handle_error(
            where=guarantee.where,
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "error": f"violated "
                         f"{get_guarantee_name(guarantee)}.{maximum_name}",
                "minimum": maximum,
                "actual": arg
            }
        )


def _check_isin(arg: Union[int, float, complex], guarantee: NumericGuarantee):
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
                "actual_type": f"{get_type_name(guarantee.isin)}"
            }
        )

    if arg not in guarantee.isin:
        handle_error(
            where=guarantee.where,
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "error": f"violated {get_guarantee_name(guarantee)}.isin",
                "isin": guarantee.isin,
                "actual": arg
            }
        )
