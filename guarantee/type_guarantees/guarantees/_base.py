"""The base of the guarantees."""


from dataclasses import dataclass
from typing import Callable


@dataclass
class Guarantee:
    name: str


@dataclass
class TypeGuarantee(Guarantee):
    warnings_only: bool = False
    force_conversion: bool = False
    callback: Callable = None
