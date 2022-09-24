"""Includes the numeric classes float, int, and complex."""


from dataclasses import dataclass
from ._base import TypeGuarantee


@dataclass
class NumericGuarantee(TypeGuarantee):
    isin: list = None
    minimum: float = None
    maximum: float = None


@dataclass
class IsFloat(NumericGuarantee):
    """
    Guarantee type float.

    Parameters
    __________

    parameter_name:     (str) (required) (position only)
                        The name of the parameter.
                        For this guarantee to work for parameters given by
                        keyword, the name has to correspond exactly to the
                        name of the parameter.

    force_conversion:   (bool) (keyword only)
                        If True, an attempt will be made to convert the
                        parameter to float.

    error_severity:     (int) (keyword only)
                        If guarantees.severity.WARN (2) or below, no Exceptions
                        will be raised. Instead, a warning will be given over
                        the command line via warnings.warn(...).
                        The severity will be mentioned in the Signal or
                        Exception.

    error_callback:     (function) (keyword only)
                        If this parameter is not None and an error occurs,
                        callback will be called with the signal corresponding to
                        the error and no other parameters.
                        No exceptions will be raised, no warnings given.
                        The purpose of callback is to allow the user to handle
                        errors themselves.

    check_function:     (function) (keyword only)
                        If this parameter is not None, this function is called
                        with the guaranteed parameter (or return value) and
                        is expected to return the parameter again (though it can
                        be changed arbitrarily -- even to None).
                        This function is meant for the user to implement their
                        own tests & checks on the parameter.

    isin:               (list) (keyword only)
                        If this parameter is not None, it must be a list of
                        floats. The parameter guaranteed with this instance of
                        IsFloat then has to have one of the values contained in
                        the list, or an exception is raised (or a warning given,
                        or callback called, depending on the other parameters to
                        IsFloat).

    minimum:            (float / int) (keyword only)
                        The minimum value of the parameter. Must be lower than
                        maximum.

    maximum:            (float / int) (keyword only)
                        The maximum value of the parameter. Must be higher than
                        minimum.

    Example
    _______

        >>> from guarantees import parameter_guarantees as pg
        >>>
        >>>
        >>> @pg.parameter_guarantees([
        >>>     pg.IsFloat(
        >>>         "param_name",           # Name of the parameter
        >>>         force_conversion=True,  # Will attempt to convert to float
        >>>         minimum=-2.2,
        >>>         maximum=2e5
        >>>     )                           # No warnings, no custom callback
        >>> ])
        >>> def fct(param_name: float):
        >>>     pass   # Some function
    """
    pass


@dataclass
class IsInt(NumericGuarantee):
    """
    Guarantee type int.

    Parameters
    __________

    parameter_name:     (str) (required) (position only)
                        The name of the parameter.
                        For this guarantee to work for parameters given by
                        keyword, the name has to correspond exactly to the
                        name of the parameter.

    force_conversion:   (bool) (keyword only)
                        If True, an attempt will be made to convert the
                        parameter to int.

    error_severity:     (int) (keyword only)
                        If guarantees.severity.WARN (2) or below, no Exceptions
                        will be raised. Instead, a warning will be given over
                        the command line via warnings.warn(...).
                        The severity will be mentioned in the Signal or
                        Exception.

    error_callback:     (function) (keyword only)
                        If this parameter is not None and an error occurs,
                        callback will be called with the signal corresponding to
                        the error and no other parameters.
                        No exceptions will be raised, no warnings given.
                        The purpose of callback is to allow the user to handle
                        errors themselves.

    check_function:     (function) (keyword only)
                        If this parameter is not None, this function is called
                        with the guaranteed parameter (or return value) and
                        is expected to return the parameter again (though it can
                        be changed arbitrarily -- even to None).
                        This function is meant for the user to implement their
                        own tests & checks on the parameter.

    isin:               (list) (keyword only)
                        If this parameter is not None, it must be a list of
                        ints. The parameter guaranteed with this instance of
                        IsInt then has to have one of the values contained in
                        the list, or an exception is raised (or a warning given,
                        or callback called, depending on the other parameters to
                        IsInt).

    minimum:            (int) (keyword only)
                        The minimum value of the parameter. Must be lower than
                        maximum.

    maximum:            (int) (keyword only)
                        The maximum value of the parameter. Must be higher than
                        minimum.

    Example
    _______

        >>> from guarantees import parameter_guarantees as pg
        >>>
        >>>
        >>> @pg.parameter_guarantees([
        >>>     pg.IsInt(
        >>>         "param_name",           # Name of the parameter
        >>>         force_conversion=True,  # Will attempt to convert to int
        >>>         minimum=-2,
        >>>         maximum=2e5
        >>>     )                           # No warnings, no custom callback
        >>> ])
        >>> def fct(param_name: int):
        >>>     pass   # Some function
    """
    pass


@dataclass
class IsComplex(NumericGuarantee):
    """
    Guarantee type complex.

    Parameters
    __________

    parameter_name:     (str) (required) (position only)
                        The name of the parameter.
                        For this guarantee to work for parameters given by
                        keyword, the name has to correspond exactly to the
                        name of the parameter.

    force_conversion:   (bool) (keyword only)
                        If True, an attempt will be made to convert the
                        parameter to complex.

    error_severity:     (int) (keyword only)
                        If guarantees.severity.WARN (2) or below, no Exceptions
                        will be raised. Instead, a warning will be given over
                        the command line via warnings.warn(...).
                        The severity will be mentioned in the Signal or
                        Exception.

    error_callback:     (function) (keyword only)
                        If this parameter is not None and an error occurs,
                        callback will be called with the signal corresponding to
                        the error and no other parameters.
                        No exceptions will be raised, no warnings given.
                        The purpose of callback is to allow the user to handle
                        errors themselves.

    check_function:     (function) (keyword only)
                        If this parameter is not None, this function is called
                        with the guaranteed parameter (or return value) and
                        is expected to return the parameter again (though it can
                        be changed arbitrarily -- even to None).
                        This function is meant for the user to implement their
                        own tests & checks on the parameter.

    isin:               (list) (keyword only)
                        If this parameter is not None, it must be a list of
                        complex numbers.
                        The parameter guaranteed with this instance of IsComplex
                        then has to have one of the values contained in
                        the list, or an exception is raised (or a warning given,
                        or callback called, depending on the other parameters to
                        IsComplex).

    minimum:            (float / int) (keyword only)
                        The minimum value of the parameter. Must be lower than
                        maximum.
                        In the case of IsComplex, this refers to the
                        absolute value of the parameter.

    maximum:            (float / int) (keyword only)
                        The maximum value of the parameter. Must be higher than
                        minimum.
                        In the case of IsComplex, this refers to the
                        absolute value of the parameter.

    minimum_re:         (float / int) (keyword only)
                        Like minimum but for the real part of the complex number
                        only.

    maximum_re:         (float / int) (keyword only)
                        Like maximum but for the real part of the complex number
                        only.

    minimum_im:         (float / int) (keyword only)
                        Like minimum but for the imaginary part of the complex
                        number only.

    maximum_im:         (float / int) (keyword only)
                        Like maximum but for the imaginary part of the complex
                        number only.
    Example
    _______

        >>> from guarantees import parameter_guarantees as pg
        >>>
        >>>
        >>> @pg.parameter_guarantees([
        >>>     pg.IsComplex(
        >>>         "param_name",           # Name of the parameter
        >>>         force_conversion=True,  # Will attempt to convert to bytes
        >>>         minimum=-2.2,
        >>>         maximum=2e5,
        >>>         minimum_re=2.,
        >>>         maximum_re=2e5,
        >>>         minimum_im=-65.,
        >>>         maximum_im=2e5
        >>>     )                           # No warnings, no custom callback
        >>> ])
        >>> def fct(param_name: complex):
        >>>     pass   # Some function
    """
    minimum_re: float = None
    maximum_re: float = None
    minimum_im: float = None
    maximum_im: float = None

