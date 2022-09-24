from dataclasses import dataclass
from typing import Callable, Type, List

from ._base import Guarantee, TypeGuarantee


@dataclass
class NoOp(Guarantee):
    """
    A buffer class to put in the place of parameters that should have no
    guarantees but have parameters with guarantees after them.

    Parameters
    __________

    parameter_name:     (str) (required) (position only)
                        The name of the parameter.
                        For this guarantee to work for parameters given by
                        keyword, the name has to correspond exactly to the
                        name of the parameter.

    Example
    _______

        >>> from guarantees import parameter_guarantees as pg
        >>>
        >>>
        >>> @pg.parameter_guarantees([
        >>>     pg.IsInt("a"),
        >>>     pg.NoOp("b"),
        >>>     pg.IsInt("c")
        >>> ])
        >>> def fct(a, b, c):
        >>>     pass

        Here, the parameters `a` and `c` are guaranteed to be of type int,
        while parameter `b` has no guarantee associated with it.

        Without the NoOp, this would not work, because the guarantees have to
        be given to `@parameter_guarantees` in the same order as to the
        function / method.
    """
    pass


@dataclass
class IsClass(TypeGuarantee):
    """
    Guarantee that the parameter is an instance of a given class.

    Parameters
    __________

    parameter_name:     (str) (required) (position only)
                        The name of the parameter.
                        For this guarantee to work for parameters given by
                        keyword, the name has to correspond exactly to the
                        name of the parameter.

    force_conversion:   (bool) (keyword only)
                        No effect in IsClass.

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

    check_fct:          (function) (keyword only)
                        If not None, this function will be given the argument
                        and is expected to return it (however modified). All
                        custom checks can be implemented here.
                        This will happen after the type of the class has been
                        checked (see member class_type).

    class_type:         (type) (keyword only)
                        IMPORTANT! Since IsClass cannot know on its own which
                        type to check for, the type has to be given to this
                        parameter.
                        If None, no check will be done.
                        Else, the parameter will be guaranteed to be of type
                        class_type.

    Example
    _______

        >>> from guarantees import parameter_guarantees as pg
        >>> import subprocess as sp
        >>> from typing import Any
        >>>
        >>>
        >>> @pg.parameter_guarantees([
        >>>     pg.IsClass(
        >>>         "param_name",           # Name of the parameter
        >>>         class_type=sp.Popen
        >>>     )                           # No warnings, no custom callback
        >>> ])
        >>> def fct(param_name: Any):
        >>>     pass   # Some function
    """
    class_type: Type = None


@dataclass
class IsNone(TypeGuarantee):
    """
    Guarantee that the parameter is None. Exists for completeness.

    Parameters
    __________

    parameter_name:     (str) (required) (position only)
                        The name of the parameter.
                        For this guarantee to work for parameters given by
                        keyword, the name has to correspond exactly to the
                        name of the parameter.

    force_conversion:   (bool) (keyword only)
                        No effect in IsNone.

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
        >>>     pg.IsNone(
        >>>         "param_name"           # Name of the parameter
        >>>     )                           # No warnings, no custom callback
        >>> ])
        >>> def fct(param_name):
        >>>     pass   # Some function
    """
    pass


@dataclass
class IsUnion(TypeGuarantee):
    """
    Guarantee that the parameter is of one of the given types (and if so,
    fulfills the other guarantees given for that type).

    Parameters
    __________

    parameter_name:     (str) (required) (position only)
                        The name of the parameter.
                        For this guarantee to work for parameters given by
                        keyword, the name has to correspond exactly to the
                        name of the parameter.

    force_conversion:   (bool) (keyword only)
                        No effect on IsUnion.

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

    guarantees:         (list) (keyword only)
                        A list of guarantees.
                        One of them has to be fully fulfilled or an exception
                        will be raised.

    Example
    _______

        >>> from guarantees import parameter_guarantees as pg
        >>>
        >>>
        >>> @pg.parameter_guarantees([
        >>>     pg.IsUnion(
        >>>         "param_name",           # Name of the parameter
        >>>         guarantees=[
        >>>             pg.IsInt("param_name", minimum=3),
        >>>             pg.IsFloat("param_name", minimum=3.)
        >>>         ]
        >>>     )                           # No warnings, no custom callback
        >>> ])
        >>> def fct(param_name: bytes):
        >>>     pass   # Some function
    """
    guarantees: List[TypeGuarantee] = None
