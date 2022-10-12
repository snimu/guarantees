from dataclasses import dataclass
from typing import Callable, Type, List

from ._base import Guarantee, TypeGuarantee


@dataclass
class NoOp(Guarantee):
    pass


@dataclass
class IsClass(TypeGuarantee):
    class_type: Type = None


@dataclass
class IsNone(TypeGuarantee):
    pass


@dataclass
class IsUnion(TypeGuarantee):
    guarantees: List[TypeGuarantee] = None
