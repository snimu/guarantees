"""The base of the classes."""


from dataclasses import dataclass
from typing import Callable


@dataclass
class Guarantee:
    parameter_name: str


@dataclass
class TypeGuarantee(Guarantee):
    warnings_only: bool = False
    force_conversion: bool = False
    callback: Callable = None
