from dataclasses import dataclass

from ._base import TypeGuarantee


@dataclass
class IsBool(TypeGuarantee):
    pass
