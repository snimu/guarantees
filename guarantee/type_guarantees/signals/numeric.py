from dataclasses import dataclass
from typing import Union, List

from guarantee.type_guarantees.signals.base import Signal


@dataclass
class SignalMinGEMax(Signal):
    arg_type: str   # The type of the signal
    minimum: Union[int, float, complex]
    maximum: Union[int, float, complex]


@dataclass
class SignalMinReGEMaxRe(SignalMinGEMax):
    arg_type = "complex"


@dataclass
class SignalMinImGEMaxIm(SignalMinGEMax):
    arg_type = "complex"


@dataclass
class SignalMinViolated(Signal):
    arg_type: str
    arg: Union[int, float, complex]
    minimum: Union[int, float, complex]


@dataclass
class SignalMinReViolated(SignalMinViolated):
    arg_type = "complex"


@dataclass
class SignalMinImViolated(SignalMinViolated):
    arg_type = "complex"


@dataclass
class SignalMaxViolated(Signal):
    arg_type: str
    arg: Union[int, float, complex]
    maximum: Union[int, float, complex]


@dataclass
class SignalMaxReViolated(SignalMaxViolated):
    arg_type = "complex"


@dataclass
class SignalMaxImViolated(SignalMaxViolated):
    arg_type = "complex"


@dataclass
class SignalNotIn(Signal):
    arg: Union[int, float, complex]
    isin: List
