from dataclasses import dataclass
from typing import Union, List


@dataclass
class Signal:
    parameter_name: str


@dataclass
class SignalTypeError(Signal):
    guarantee_type_name: str
    should_type_name: str
    is_type_name: str
    force_conversion: bool = False


@dataclass
class SignalMinLenGEMaxLen(Signal):
    guarantee_type_name: str
    minimum_len: int
    maximum_len: int


@dataclass
class SignalMinLenViolated(Signal):
    guarantee_type_name: str
    arg: Union[list, tuple, dict, set, frozenset, range]
    minimum_len: int


@dataclass
class SignalMaxLenViolated(Signal):
    guarantee_type_name: str
    arg: Union[list, tuple, dict, set, frozenset, range]
    maximum_len: int


@dataclass
class SignalNotIn(Signal):
    guarantee_type_name: str
    arg: Union[int, float, complex, str]
    isin: List
