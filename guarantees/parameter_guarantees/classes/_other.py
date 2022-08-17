from dataclasses import dataclass
from typing import Callable, Type

from ._base import Guarantee, TypeGuarantee


@dataclass
class NoOp(Guarantee):
    """
    A buffer class to put in the place of parameters that should have no
    guarantees but have parameters with guarantees after them.

    Example:

        >>> @parameter_guarantees([
        >>>     IsInt("a"),
        >>>     NoOp("b"),
        >>>     IsInt("c")
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
    class_type: Type = None
    callback: Callable = None    # Take signals, return None
    check_fct: Callable = None   # Take arg, return arg (optionally changed)


@dataclass
class IsNone(TypeGuarantee):
    pass
