from typing import Union

from guarantees.parameter_guarantees.classes import IsInt, IsFloat, IsComplex, \
    NumericGuarantee
from guarantees.parameter_guarantees.signals.common import SignalTypeError, \
    SignalNotIn
from guarantees.parameter_guarantees.signals.numeric import \
    SignalMinGEMax, SignalMinReGEMaxRe, SignalMinImGEMaxIm,\
    SignalMinViolated, SignalMinReViolated, SignalMinImViolated, \
    SignalMaxViolated, SignalMaxReViolated, SignalMaxImViolated
from guarantees.parameter_guarantees.enforcement._util import \
    raise_value_warning_or_exception, raise_type_warning_or_exception, \
    get_guaranteed_type, get_guaranteed_type_name, get_guarantee_name, \
    get_type_name, get_err_msg_type, get_err_msg_minimum_ge_maximum, \
    get_err_msg_minimum, get_err_msg_maximum, get_err_msg_isin


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

    if guarantee.check_function is not None:
        arg = guarantee.check_function(arg)

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

    if guarantee.check_function is not None:
        arg = guarantee.check_function(arg)

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

    if guarantee.check_function is not None:
        arg = guarantee.check_function(arg)

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

    # Handle errors
    if not err:
        return arg

    # Error occurred

    signal = SignalTypeError(
        parameter_name=guarantee.parameter_name,
        guarantee_type_name=get_guaranteed_type_name(guarantee),
        should_type_name=type_should_str,
        is_type_name=type_is_str,
        force_conversion=guarantee.force_conversion
    )
    if guarantee.error_callback is not None:
        guarantee.error_callback(signal)
    else:
        err_msg = get_err_msg_type(signal)
        raise_type_warning_or_exception(err_msg, guarantee)


def _check_minimum_type(
        minimum: Union[int, float],
        guarantee: NumericGuarantee
) -> None:
    if type(minimum) not in [int, float]:
        err_msg = f"parameter: {get_guarantee_name(guarantee)}.minimum \n" \
                  f"\t violated: type -- guarantee parameter \n" \
                  f"\t should: {get_guaranteed_type_name(guarantee)} \n" \
                  f"\t actual: {get_type_name(minimum)} \n"
        raise_type_warning_or_exception(err_msg, guarantee)


def _check_maximum_type(
        maximum: Union[int, float],
        guarantee: NumericGuarantee
) -> None:
    if type(maximum) not in [int, float]:
        err_msg = f"parameter: {get_guarantee_name(guarantee)}.maximum \n" \
                  f"\t violated: type -- guarantee parameter \n" \
                  f"\t should: {get_guaranteed_type_name(guarantee)} \n" \
                  f"\t actual: {get_type_name(maximum)} \n"
        raise_type_warning_or_exception(err_msg, guarantee)


def _check_min_ge_max(
        guarantee: NumericGuarantee,
        minimum: Union[int, float, complex],
        maximum: Union[int, float, complex],
        minmax_type: str = "abs"
) -> None:
    if minimum is not None and maximum is not None and minimum >= maximum:
        _check_minimum_type(minimum, guarantee)
        _check_maximum_type(maximum, guarantee)

        signal = SignalMinGEMax
        if minmax_type == "re":
            signal = SignalMinReGEMaxRe
        elif minmax_type == "im":
            signal = SignalMinImGEMaxIm
        signal = signal(
            parameter_name=guarantee.parameter_name,
            guarantee_type_name=get_guaranteed_type_name(guarantee),
            minimum=minimum,
            maximum=maximum
        )

        if guarantee.error_callback is not None:
            guarantee.error_callback(signal)
        else:
            err_msg = get_err_msg_minimum_ge_maximum(signal)
            raise_value_warning_or_exception(err_msg, guarantee)


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
        signal = SignalMinViolated
        if min_type == "re":
            signal = SignalMinReViolated
        if min_type == "im":
            signal = SignalMinImViolated

        signal = signal(
            parameter_name=guarantee.parameter_name,
            guarantee_type_name=get_guarantee_name(guarantee),
            arg=arg,
            minimum=minimum
        )

        if guarantee.error_callback is not None:
            guarantee.error_callback(signal)
        else:
            err_msg = get_err_msg_minimum(signal)
            raise_value_warning_or_exception(err_msg, guarantee)


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
        signal = SignalMaxViolated
        if max_type == "re":
            signal = SignalMaxReViolated
        if max_type == "im":
            signal = SignalMaxImViolated

        signal = signal(
            parameter_name=guarantee.parameter_name,
            guarantee_type_name=get_guarantee_name(guarantee),
            arg=arg,
            maximum=maximum
        )
        if guarantee.error_callback is not None:
            guarantee.error_callback(signal)
        else:
            err_msg = get_err_msg_maximum(signal)
            raise_value_warning_or_exception(err_msg, guarantee)


def _check_isin(arg: Union[int, float, complex], guarantee: NumericGuarantee):
    if guarantee.isin is None:
        return

    if type(guarantee.isin) is not list:
        err_msg = f"parameter: {get_guarantee_name(guarantee)}.isin \n" \
                  f"\t violated: type -- guarantee parameter \n" \
                  f"\t should: list \n" \
                  f"\t actual: {get_type_name(guarantee.isin)} \n"
        raise_type_warning_or_exception(err_msg, guarantee)

    if arg in guarantee.isin:
        return

    signal = SignalNotIn(
        parameter_name=guarantee.parameter_name,
        guarantee_type_name=get_guarantee_name(guarantee),
        arg=arg,
        isin=guarantee.isin
    )
    if guarantee.error_callback is not None:
        guarantee.error_callback(signal)
    else:
        err_msg = get_err_msg_isin(signal)
        raise_value_warning_or_exception(err_msg, guarantee)
