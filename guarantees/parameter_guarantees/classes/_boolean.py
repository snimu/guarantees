from dataclasses import dataclass

from ._base import TypeGuarantee


@dataclass
class IsBool(TypeGuarantee):
    """
    Guarantee type bool.

    Parameters
    __________

    parameter_name:     (str) (required) (position only)
                        The name of the parameter.
                        For this guarantee to work for parameters given by
                        keyword, the name has to correspond exactly to the
                        name of the parameter.

    force_conversion:   (bool) (keyword only)
                        If True, an attempt will be made to convert the
                        parameter to bool.

    warnings_only:      (bool) (keyword only)
                        If True, no Exceptions will be raised. Instead,
                        a warning will be given over the command line via
                        warnings.warn(...).

    callback:           (function) (keyword only)
                        If this parameter is not None and an error occurs,
                        callback will be called with the signal corresponding to
                        the error and no other parameters.
                        No exceptions will be raised, no warnings given.
                        The purpose of callback is to allow the user to handle
                        errors themselves.

    Example
    _______

        >>> from guarantees import parameter_guarantees as pg
        >>>
        >>>
        >>> @pg.parameter_guarantees([
        >>>     pg.IsBool(
        >>>         "param_name",           # Name of the parameter
        >>>         force_conversion=True   # Will attempt to convert to bytes
        >>>     )                           # No warnings, no custom callback
        >>> ])
        >>> def fct(param_name: bool):
        >>>     pass   # Some function
    """
    pass
