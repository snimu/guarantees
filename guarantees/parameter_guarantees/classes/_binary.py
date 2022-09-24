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

    warnings_only:      (bool) (keyword only)
                        If True, no Exceptions will be raised. Instead,
                        a warning will be given over the command line via
                        warnings.warn(...).

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

        >>> from guarantees import parameter_guarantees as pg
        >>>
        >>>
        >>> @pg.parameter_guarantees([
        >>>     pg.IsBytes(
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

    warnings_only:      (bool) (keyword only)
                        If True, no Exceptions will be raised. Instead,
                        a warning will be given over the command line via
                        warnings.warn(...).

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

        >>> from guarantees import parameter_guarantees as pg
        >>>
        >>>
        >>> @pg.parameter_guarantees([
        >>>     pg.IsByteArray(
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

    warnings_only:      (bool) (keyword only)
                        If True, no Exceptions will be raised. Instead,
                        a warning will be given over the command line via
                        warnings.warn(...).

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

        >>> from guarantees import parameter_guarantees as pg
        >>>
        >>>
        >>> @pg.parameter_guarantees([
        >>>     pg.IsMemoryView(
        >>>         "param_name",           # Name of the parameter
        >>>         force_conversion=True   # Will attempt to convert to bytes
        >>>     )                           # No warnings, no custom callback
        >>> ])
        >>> def fct(param_name: memoryview):
        >>>     pass   # Some function
    """
    pass
