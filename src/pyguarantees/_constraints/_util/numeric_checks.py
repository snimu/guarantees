from typing import Union

from pyguarantees._constraints._util.error_handeling import handle_error
from pyguarantees._constraints._util.typenames import get_arg_type_name


def _check_minimum_type(
        minimum: Union[int, float],
        guarantee
) -> None:
    if type(minimum) not in [int, float]:
        handle_error(
            where="internal",
            type_or_value="type",
            guarantee=guarantee,
            parameter_name=f"{guarantee.guarantee_name}.minimum",
            what_dict={
                "should_type": \
                    "int" if type(guarantee.guaranteed_type) is int else "float",
                "actual_type": get_arg_type_name(minimum)
            }
        )


def _check_maximum_type(
        maximum: Union[int, float],
        guarantee
) -> None:
    if type(maximum) not in [int, float]:
        handle_error(
            where="internal",
            type_or_value="type",
            guarantee=guarantee,
            parameter_name=f"{guarantee.guarantee_name}.maximum",
            what_dict={
                "should_type": \
                    "int" if type(guarantee.guaranteed_type) is int else "float",
                "actual_type": get_arg_type_name(maximum)
            }
        )


def check_min_ge_max(
        guarantee,
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
            parameter_name=f"{guarantee.guarantee_name}.{minimum_name} "
                           f"and {get_arg_type_name(guarantee)}.{maximum_name}",
            what_dict={
                "error": f"{minimum_name} >= {maximum_name} ",
                "minimum": str(minimum),
                "maximum": str(maximum)
            }
        )


def check_min(
        arg: Union[int, float, complex],
        minimum: Union[int, float, complex],
        guarantee,
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
                         f"{guarantee.guarantee_name}.{minimum_name}",
                minimum_name: minimum,
                "actual": arg
            }
        )


def check_max(
        arg: Union[int, float, complex],
        maximum: Union[int, float, complex],
        guarantee,
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
                         f"{guarantee.guarantee_name}.{maximum_name}",
                maximum_name: maximum,
                "actual": arg
            }
        )


def check_isin(arg: Union[int, float, complex], guarantee):
    if guarantee.isin is None:
        return

    if type(guarantee.isin) is not list:
        handle_error(
            where="internal",
            type_or_value="type",
            guarantee=guarantee,
            parameter_name=f"{guarantee.guarantee_name}.isin",
            what_dict={
                "should_type": "list",
                "actual_type": f"{get_arg_type_name(guarantee.isin)}"
            }
        )

    if arg not in guarantee.isin:
        handle_error(
            where=guarantee.where,
            type_or_value="value",
            guarantee=guarantee,
            parameter_name=guarantee.parameter_name,
            what_dict={
                "error": f"violated {guarantee.guarantee_name}.isin",
                "isin": guarantee.isin,
                "actual": arg
            }
        )