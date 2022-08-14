from dataclasses import dataclass
from typing import Callable

from ._base import Guarantee, TypeGuarantee


@dataclass
class NoOp(Guarantee):
    pass


@dataclass
class IsClass(TypeGuarantee):
    class_type: object = None
    callback: Callable = None    # Take signals, return None
    check_fct: Callable = None   # Take arg, return arg (optionally changed)
