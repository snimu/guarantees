"""The base of the classes."""


from dataclasses import dataclass
from typing import Callable
from guarantees import severity


@dataclass
class Guarantee:
    parameter_name: str
    function_name: str = ""
    function_namespace: str = ""


@dataclass
class TypeGuarantee(Guarantee):
    where: str = "parameter"
    error_severity: int = severity.ERROR
    force_conversion: bool = False
    error_callback: Callable = None
    check_function: Callable = None  # Take arg, return arg (optionally changed)
