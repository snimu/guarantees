from dataclasses import dataclass
from typing import Callable, List

from ._base import TypeGuarantee


@dataclass
class IsStr(TypeGuarantee):
    minimum_len: int = None
    maximum_len: int = None
    isin: List = None
