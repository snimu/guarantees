from dataclasses import dataclass
from typing import Union

from guarantees.parameter_guarantees.signals.base import Signal


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


@dataclass
class SignalContainsViolated(Signal):
    arg_type: str
    arg: Union[list, tuple, set, frozenset]
    contains: list


@dataclass
class SignalHasKeysViolated(Signal):
    arg_type: str
    arg: dict
    has_keys: list


@dataclass
class SignalHasValuesViolated(Signal):
    arg_type: str
    arg: dict
    has_values: list
