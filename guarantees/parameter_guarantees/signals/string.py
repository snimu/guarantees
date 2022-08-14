from dataclasses import dataclass
from typing import List

from guarantees.parameter_guarantees.signals.base import Signal


@dataclass
class SignalMaximumLenViolated(Signal):
    arg: str
    maximum_len: int


@dataclass
class SignalMinimumLenViolated(Signal):
    arg: str
    minimum_len: int


@dataclass
class SignalMinimumLenGEMaximumLen(Signal):
    arg_type: str
    minimum_len: int
    maximum_len: int


@dataclass
class SignalNotIn(Signal):
    arg: str
    isin: List
