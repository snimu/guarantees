from dataclasses import dataclass

from ._base import TypeGuarantee


@dataclass
class IsBytes(TypeGuarantee):
    """
    Guarantee type bytes.

    Parameters
    __________

    parameter_name:     (str) (required) (position only)
                        The name of the parameter.
                        For this guarantee to work for parameters given by
                        keyword, the name has to correspond exactly to the
                        name of the parameter.

    force_conversion:   (bool) (keyword only)
                        If True, an attempt will be made to convert the
                        parameter to bytes.

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

    Example
    _______

        >>> from guarantees import functional_guarantees as fg
        >>>
        >>>
        >>> @fg.parameter_guarantees([
        >>>     fg.IsBytes(
        >>>         "param_name",           # Name of the parameter
        >>>         force_conversion=True   # Will attempt to convert to bytes
        >>>     )                           # No warnings, no custom callback
        >>> ])
        >>> def fct(param_name: bytes):
        >>>     pass   # Some function
    """
    pass


@dataclass
class IsByteArray(TypeGuarantee):
    """
    Guarantee type bytearray.

    Parameters
    __________

    parameter_name:     (str) (required) (position only)
                        The name of the parameter.
                        For this guarantee to work for parameters given by
                        keyword, the name has to correspond exactly to the
                        name of the parameter.

    force_conversion:   (bool) (keyword only)
                        If True, an attempt will be made to convert the
                        parameter to bytearray.

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

    Example
    _______

        >>> from guarantees import functional_guarantees as fg
        >>>
        >>>
        >>> @fg.parameter_guarantees([
        >>>     fg.IsByteArray(
        >>>         "param_name",           # Name of the parameter
        >>>         force_conversion=True   # Will attempt to convert to bytes
        >>>     )                           # No warnings, no custom callback
        >>> ])
        >>> def fct(param_name: bytearray):
        >>>     pass   # Some function
    """
    pass


@dataclass
class IsMemoryView(TypeGuarantee):
    """
    Guarantee type memoryview.

    Parameters
    __________

    parameter_name:     (str) (required) (position only)
                        The name of the parameter.
                        For this guarantee to work for parameters given by
                        keyword, the name has to correspond exactly to the
                        name of the parameter.

    force_conversion:   (bool) (keyword only)
                        If True, an attempt will be made to convert the
                        parameter to memoryview.

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

    Example
    _______

        >>> from guarantees import functional_guarantees as fg
        >>>
        >>>
        >>> @fg.parameter_guarantees([
        >>>     fg.IsMemoryView(
        >>>         "param_name",           # Name of the parameter
        >>>         force_conversion=True   # Will attempt to convert to bytes
        >>>     )                           # No warnings, no custom callback
        >>> ])
        >>> def fct(param_name: memoryview):
        >>>     pass   # Some function
    """
    pass
