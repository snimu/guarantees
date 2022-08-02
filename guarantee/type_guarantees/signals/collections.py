from dataclasses import dataclass
from typing import Union

from guarantee.type_guarantees.signals.base import Signal


@dataclass
class SignalMinLenGEMaxLen(Signal):
    arg_type: str  # The type of the signal
    minimum_len: int
    maximum_len: int


@dataclass
class SignalMinLenViolated(Signal):
    arg_type: str
    arg: Union[list, tuple, dict, set, frozenset, range]
    minimum_len: int


@dataclass
class SignalMaxLenViolated(Signal):
    arg_type: str
    arg: Union[list, tuple, dict, set, frozenset, range]
    maximum_len: int
