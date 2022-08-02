import warnings
from typing import Union

from guarantee.type_guarantees.guarantees import IsInt, IsFloat, IsComplex, \
    NumericGuarantee
from guarantee.type_guarantees.signals.base import SignalTypeError
from guarantee.type_guarantees.signals.numeric import \
    SignalMinGEMax, SignalMinReGEMaxRe, SignalMinImGEMaxIm,\
    SignalMinViolated, SignalMinReViolated, SignalMinImViolated, \
    SignalMaxViolated, SignalMaxReViolated, SignalMaxImViolated, \
    SignalNotIn


def enforce_isint(arg: int, guarantee: IsInt) -> int:
    arg = _check_type(arg, guarantee)

    _check_min_ge_max(
        guarantee=guarantee,
        arg_type="int",
        minimum=guarantee.minimum,
        maximum=guarantee.maximum
    )

    _check_min(arg, guarantee.minimum, guarantee, "int")
    _check_max(arg, guarantee.maximum, guarantee, "int")

    _check_isin(arg, guarantee)

    return arg


def enforce_isfloat(arg: float, guarantee: IsFloat) -> float:
    arg = _check_type(arg, guarantee)

    _check_min_ge_max(
        guarantee=guarantee,
        arg_type="float",
        minimum=guarantee.minimum,
        maximum=guarantee.maximum
    )

    _check_min(arg, guarantee.minimum, guarantee, "float")
    _check_max(arg, guarantee.maximum, guarantee, "float")

    _check_isin(arg, guarantee)

    return arg


def enforce_iscomplex(arg: complex, guarantee: IsComplex) -> complex:
    arg = _check_type(arg, guarantee)

    _check_min_ge_max(
        guarantee=guarantee,
        arg_type="complex",
        minimum=guarantee.minimum,
        maximum=guarantee.maximum
    )
    _check_min_ge_max(
        guarantee=guarantee,
        arg_type="complex",
        minimum=guarantee.minimum_re,
        maximum=guarantee.maximum_re,
        minmax_type="re"
    )
    _check_min_ge_max(
        guarantee=guarantee,
        arg_type="complex",
        minimum=guarantee.minimum_im,
        maximum=guarantee.maximum_im,
        minmax_type="im"
    )

    _check_min(abs(arg), guarantee.minimum, guarantee, "complex")
    _check_max(abs(arg), guarantee.maximum, guarantee, "complex")
    _check_min(arg.real, guarantee.minimum_re, guarantee, "complex", "re")
    _check_max(arg.real, guarantee.maximum_re, guarantee, "complex", "re")
    _check_min(arg.imag, guarantee.minimum_im, guarantee, "complex", "im")
    _check_max(arg.imag, guarantee.maximum_im, guarantee, "complex", "im")

    _check_isin(arg, guarantee)

    return arg


def _check_type(
        arg: Union[int, float, complex],
        guarantee: NumericGuarantee
) -> Union[int, float, complex]:
    if isinstance(guarantee, IsInt):
        type_should_str = "int"
        type_should = int
    elif isinstance(guarantee, IsFloat):
        type_should_str = "float"
        type_should = float
    elif isinstance(guarantee, IsComplex):
        type_should_str = "complex"
        type_should = complex
    else:
        raise TypeError("Error in library: wrong guarantee given.")

    if type(arg) is int:
        type_is_str = "int"
    elif type(arg) is float:
        type_is_str = "float"
    elif type(arg) is complex:
        type_is_str = "complex"
    else:
        # The following produces an ugly string but works
        type_is_str = str(type(arg))

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
    if guarantee.callback is not None:
        guarantee.callback(
            SignalTypeError(
                arg_name=guarantee.name,
                type_should=type_should_str,
                type_is=type_is_str,
                force_conversion=guarantee.force_conversion
            )
        )
    else:
        err_msg = f"Guaranteed type {type_should_str} " \
                  f"for parameter {guarantee.name}, " \
                  f"but received type {type_is_str}. " \
                  f"Called with force_conversion={guarantee.force_conversion}"
        if guarantee.warnings_only:
            warnings.warn(err_msg)
        else:
            raise TypeError(err_msg)


def _check_min_ge_max(
        guarantee: NumericGuarantee,
        arg_type: str,
        minimum: Union[int, float, complex],
        maximum: Union[int, float, complex],
        minmax_type: str = "abs"
) -> None:
    if minimum is not None and maximum is not None and minimum >= maximum:
        if guarantee.callback is not None:
            sig = SignalMinGEMax
            if minmax_type == "re":
                sig = SignalMinReGEMaxRe
            elif minmax_type == "im":
                sig = SignalMinImGEMaxIm

            guarantee.callback(
                sig(
                    arg_name=guarantee.name,
                    arg_type=arg_type,
                    minimum=minimum,
                    maximum=maximum
                )
            )
        else:
            minstr, maxstr = "minimum", "maximum"
            if minmax_type == "re":
                minstr, maxstr = "minimum_re", "maximum_re"
            if minmax_type == "im":
                minstr, maxstr = "minimum_im", "maximum_im"

            err_msg = f"You guaranteed parameter type {arg_type} with " \
                      f"{minstr} {minimum} >= {maxstr} {maximum}; " \
                      f"{minstr} must be smaller than {maxstr}."
            if guarantee.warnings_only:
                warnings.warn(err_msg)
            else:
                raise ValueError(err_msg)


def _check_min(
        arg: Union[int, float, complex],
        minimum: Union[int, float, complex],
        guarantee: NumericGuarantee,
        arg_type: str,
        min_type: str = "abs"
) -> None:
    if minimum is None:
        return

    if type(minimum) not in [int, float, complex]:
        err_msg = f"The parameter 'minimum' must be of type {type(arg)} " \
                  f"but is of type {type(minimum)}. "
        if guarantee.warnings_only:
            warnings.warn(err_msg + "Minimum will not be checked.")
        else:
            raise TypeError(err_msg)

    if arg < minimum:
        if guarantee.callback is not None:
            sig = SignalMinViolated
            if min_type == "re":
                sig = SignalMinReViolated
            if min_type == "im":
                sig = SignalMinImViolated

            guarantee.callback(
                sig(
                    arg_name=guarantee.name,
                    arg_type=arg_type,
                    arg=arg,
                    minimum=minimum
                )
            )
        else:
            minstr = "minimum"
            minstr = "minimum_re" if min_type == "re" else minstr
            minstr = "minimum_im" if min_type == "im" else minstr

            err_msg = f"You guaranteed parameter type {arg_type} with " \
                      f"{minstr} {minimum}. Argument {guarantee.name} " \
                      f"has been received with value {arg} < {minimum}."
            if guarantee.warnings_only:
                warnings.warn(err_msg)
            else:
                raise ValueError(err_msg)


def _check_max(
        arg: Union[int, float, complex],
        maximum: Union[int, float, complex],
        guarantee: NumericGuarantee,
        arg_type: str,
        max_type: str = "abs"
) -> None:
    if maximum is None:
        return

    if type(maximum) not in [int, float, complex]:
        err_msg = f"The parameter 'maximum' must be of type {type(arg)} " \
                  f"but is of type {type(maximum)}. "
        if guarantee.warnings_only:
            warnings.warn(err_msg + "Maximum will not be checked.")
        else:
            raise TypeError(err_msg)

    if arg > maximum:
        if guarantee.callback is not None:
            sig = SignalMaxViolated
            if max_type == "re":
                sig = SignalMaxReViolated
            if max_type == "im":
                sig = SignalMaxImViolated

            guarantee.callback(
                sig(
                    arg_name=guarantee.name,
                    arg_type=arg_type,
                    arg=arg,
                    maximum=maximum
                )
            )
        else:
            maxstr = "maximum"
            maxstr = "maximum_re" if max_type == "re" else maxstr
            maxstr = "maximum_im" if max_type == "im" else maxstr

            err_msg = f"You guaranteed parameter type {arg_type} with " \
                      f"{maxstr} {maximum}. Argument {guarantee.name} " \
                      f"has been received with value {arg} > {maximum}."
            if guarantee.warnings_only:
                warnings.warn(err_msg)
            else:
                raise ValueError(err_msg)


def _check_isin(arg: Union[int, float, complex], guarantee: NumericGuarantee):
    if guarantee.isin is None:
        return

    if type(guarantee.isin) not in [list, tuple]:
        err_msg = "The parameter 'isin' must be of type list or tuple. " \
                  "Returning."
        if guarantee.warnings_only:
            warnings.warn(err_msg)
            return
        else:
            raise TypeError(err_msg)

    if arg in guarantee.isin:
        return

    if guarantee.callback is not None:
        guarantee.callback(
            SignalNotIn(
                arg_name=guarantee.name,
                arg=arg,
                isin=guarantee.isin
            )
        )
    else:
        err_msg = f"The parameter {guarantee.name} " \
                  f"must be in {guarantee.isin}. " \
                  f"It is not. Value: {arg}"
        if guarantee.warnings_only:
            warnings.warn(err_msg)
        else:
            raise ValueError(err_msg)
