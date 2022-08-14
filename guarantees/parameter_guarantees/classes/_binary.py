from dataclasses import dataclass

from ._base import TypeGuarantee


@dataclass
class IsBytes(TypeGuarantee):
    pass


@dataclass
class IsByteArray(TypeGuarantee):
    pass


@dataclass
class IsMemoryView(TypeGuarantee):
    pass
