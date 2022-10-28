"""The base of the classes."""


from dataclasses import dataclass
from typing import Callable, Union, Dict, List
from guarantees import severity


@dataclass
class Guarantee:
    parameter_name: str
    qualname: str = ""
    module: str = ""
    where: str = "parameter"


@dataclass
class TypeGuarantee(Guarantee):
    error_severity: int = severity.ERROR
    force_conversion: bool = False
    error_callback: Callable = None
    check_functions: \
        Union[
            List[Callable],
            Dict[Callable, str],
            Dict[str, Callable]
        ] = None
