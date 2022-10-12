from dataclasses import dataclass
from typing import Any, List

from ._base import TypeGuarantee


@dataclass
class CollectionType(TypeGuarantee):
    minimum_len: int = None
    maximum_len: int = None


@dataclass
class IsList(CollectionType):
    contains: List[Any] = None


@dataclass
class IsTuple(CollectionType):
    contains: List[Any] = None


@dataclass
class IsDict(CollectionType):
    has_keys: List[Any] = None
    has_values: List[Any] = None


@dataclass
class IsSet(CollectionType):
    contains: Any = None


@dataclass
class IsFrozenSet(CollectionType):
    contains: Any = None


@dataclass
class IsRange(TypeGuarantee):
    pass
