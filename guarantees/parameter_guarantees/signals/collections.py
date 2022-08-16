from dataclasses import dataclass
from typing import Union

from guarantees.parameter_guarantees.signals.base import Signal


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
class SignalContainsViolated(Signal):
    guarantee_type_name: str
    arg: Union[list, tuple, set, frozenset]
    contains: list


@dataclass
class SignalHasKeysViolated(Signal):
    guarantee_type_name: str
    arg: dict
    has_keys: list


@dataclass
class SignalHasValuesViolated(Signal):
    guarantee_type_name: str
    arg: dict
    has_values: list
