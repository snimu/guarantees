from dataclasses import dataclass
from typing import Any, List

from ._base import TypeGuarantee


@dataclass
class CollectionType(TypeGuarantee):
    minimum_len: int = None
    maximum_len: int = None


@dataclass
class IsList(CollectionType):
    """
    Guarantee type list.

    Parameters
    __________

    parameter_name:     (str) (required) (position only)
                        The name of the parameter.
                        For this guarantee to work for parameters given by
                        keyword, the name has to correspond exactly to the
                        name of the parameter.

    force_conversion:   (bool) (keyword only)
                        If True, an attempt will be made to convert the
                        parameter to list.

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

    minimum_len:        (int) (keyword only)
                        Guarantees that the length of the list is at least
                        minimum_len.

    maximum_len:        (int) (keyword only)
                        Guarantees that the length of the list is at most
                        maximum_len.
                        Must be greater than minimum_len if both are
                        not None.

    contains:           (list) (keyword only)
                        A list of items that must be contained within the
                        list.

    Example
    _______

        >>> from guarantees import functional_guarantees as fg
        >>>
        >>>
        >>> @fg.parameter_guarantees([
        >>>     fg.IsList(
        >>>         "param_name",           # Name of the parameter
        >>>         force_conversion=True,  # Will attempt to convert to bytes
        >>>         minimum_len=3,
        >>>         maximum_len=200
        >>>     )                           # No warnings, no custom callback
        >>> ])
        >>> def fct(param_name: list):
        >>>     pass   # Some function
    """
    contains: List[Any] = None


@dataclass
class IsTuple(CollectionType):
    """
    Guarantee type tuple.

    Parameters
    __________

    parameter_name:     (str) (required) (position only)
                        The name of the parameter.
                        For this guarantee to work for parameters given by
                        keyword, the name has to correspond exactly to the
                        name of the parameter.

    force_conversion:   (bool) (keyword only)
                        If True, an attempt will be made to convert the
                        parameter to tuple.

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

    minimum_len:        (int) (keyword only)
                        Guarantees that the length of the tuple is at least
                        minimum_len.

    maximum_len:        (int) (keyword only)
                        Guarantees that the length of the tuple is at most
                        maximum_len.
                        Must be greater than minimum_len if both are
                        not None.

    contains:           (list) (keyword only)
                        A list of items that must be contained within the
                        tuple.

    Example
    _______

        >>> from guarantees import functional_guarantees as fg
        >>>
        >>>
        >>> @fg.parameter_guarantees([
        >>>     fg.IsTuple(
        >>>         "param_name",           # Name of the parameter
        >>>         force_conversion=True,  # Will attempt to convert to bytes
        >>>         minimum_len=3,
        >>>         maximum_len=200
        >>>     )                           # No warnings, no custom callback
        >>> ])
        >>> def fct(param_name: tuple):
        >>>     pass   # Some function
    """
    contains: List[Any] = None


@dataclass
class IsDict(CollectionType):
    """
    Guarantee type list.

    Parameters
    __________

    parameter_name:     (str) (required) (position only)
                        The name of the parameter.
                        For this guarantee to work for parameters given by
                        keyword, the name has to correspond exactly to the
                        name of the parameter.

    force_conversion:   (bool) (keyword only)
                        If True, an attempt will be made to convert the
                        parameter to list.

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

    minimum_len:        (int) (keyword only)
                        Guarantees that the length of the list is at least
                        minimum_len.

    maximum_len:        (int) (keyword only)
                        Guarantees that the length of the list is at most
                        maximum_len.
                        Must be greater than minimum_len if both are
                        not None.

    has_keys:           (list) (keyword only)
                        A list of items that must be contained within the
                        keys of the dict.

    has_values:         (list) (keyword only)
                        A list of items that must be contained within the
                        values.


    Example
    _______

        >>> from guarantees import functional_guarantees as fg
        >>>
        >>>
        >>> @fg.parameter_guarantees([
        >>>     fg.IsDict(
        >>>         "param_name",           # Name of the parameter
        >>>         force_conversion=True,  # Will attempt to convert to bytes
        >>>         minimum_len=3,
        >>>         maximum_len=200
        >>>     )                           # No warnings, no custom callback
        >>> ])
        >>> def fct(param_name: dict):
        >>>     pass   # Some function
    """
    has_keys: List[Any] = None
    has_values: List[Any] = None


@dataclass
class IsSet(CollectionType):
    """
    Guarantee type set.

    Parameters
    __________

    parameter_name:     (str) (required) (position only)
                        The name of the parameter.
                        For this guarantee to work for parameters given by
                        keyword, the name has to correspond exactly to the
                        name of the parameter.

    force_conversion:   (bool) (keyword only)
                        If True, an attempt will be made to convert the
                        parameter to set.

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

    minimum_len:        (int) (keyword only)
                        Guarantees that the length of the set is at least
                        minimum_len.

    maximum_len:        (int) (keyword only)
                        Guarantees that the length of the set is at most
                        maximum_len.
                        Must be greater than minimum_len if both are
                        not None.

    contains:           (list) (keyword only)
                        A list of items that must be contained within the
                        set.

    Example
    _______

        >>> from guarantees import functional_guarantees as fg
        >>>
        >>>
        >>> @fg.parameter_guarantees([
        >>>     fg.IsSet(
        >>>         "param_name",           # Name of the parameter
        >>>         force_conversion=True,  # Will attempt to convert to bytes
        >>>         minimum_len=3,
        >>>         maximum_len=200
        >>>     )                           # No warnings, no custom callback
        >>> ])
        >>> def fct(param_name: set):
        >>>     pass   # Some function
    """
    contains: Any = None


@dataclass
class IsFrozenSet(CollectionType):
    """
    Guarantee type frozenset.

    Parameters
    __________

    parameter_name:     (str) (required) (position only)
                        The name of the parameter.
                        For this guarantee to work for parameters given by
                        keyword, the name has to correspond exactly to the
                        name of the parameter.

    force_conversion:   (bool) (keyword only)
                        If True, an attempt will be made to convert the
                        parameter to frozenset.

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

    minimum_len:        (int) (keyword only)
                        Guarantees that the length of the frozenset is at least
                        minimum_len.

    maximum_len:        (int) (keyword only)
                        Guarantees that the length of the frozenset is at most
                        maximum_len.
                        Must be greater than minimum_len if both are
                        not None.

    contains:           (list) (keyword only)
                        A list of items that must be contained within the
                        frozenset.

    Example
    _______

        >>> from guarantees import functional_guarantees as fg
        >>>
        >>>
        >>> @fg.parameter_guarantees([
        >>>     fg.IsFrozenSet(
        >>>         "param_name",           # Name of the parameter
        >>>         force_conversion=True,  # Will attempt to convert to bytes
        >>>         minimum_len=3,
        >>>         maximum_len=200
        >>>     )                           # No warnings, no custom callback
        >>> ])
        >>> def fct(param_name: frozenset):
        >>>     pass   # Some function
    """
    contains: Any = None


@dataclass
class IsRange(TypeGuarantee):
    """
    Guarantee type range.

    Parameters
    __________

    parameter_name:     (str) (required) (position only)
                        The name of the parameter.
                        For this guarantee to work for parameters given by
                        keyword, the name has to correspond exactly to the
                        name of the parameter.

    force_conversion:   (bool) (keyword only)
                        If True, an attempt will be made to convert the
                        parameter to range.

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

    minimum_len:        (int) (keyword only)
                        Guarantees that the length of the range is at least
                        minimum_len.

    maximum_len:        (int) (keyword only)
                        Guarantees that the length of the range is at most
                        maximum_len.
                        Must be greater than minimum_len if both are
                        not None.

    Example
    _______

        >>> from guarantees import functional_guarantees as fg
        >>>
        >>>
        >>> @fg.parameter_guarantees([
        >>>     fg.IsRange(
        >>>         "param_name",           # Name of the parameter
        >>>         force_conversion=True,  # Will attempt to convert to bytes
        >>>         minimum_len=3,
        >>>         maximum_len=200
        >>>     )                           # No warnings, no custom callback
        >>> ])
        >>> def fct(param_name: range):
        >>>     pass   # Some function
    """
    pass
