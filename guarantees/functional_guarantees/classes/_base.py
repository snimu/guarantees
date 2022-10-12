"""The base of the classes."""


from dataclasses import dataclass
from typing import Callable, Union, Dict
from guarantees import severity


@dataclass
class Guarantee:
    parameter_name: str
    function_name: str = ""
    function_namespace: str = ""
    where: str = "parameter"


@dataclass
class TypeGuarantee(Guarantee):
    error_severity: int = severity.ERROR
    force_conversion: bool = False
    error_callback: Callable = None
    check_functions: \
        Union[Callable, Dict[Callable, str], Dict[str, Callable]] = None
