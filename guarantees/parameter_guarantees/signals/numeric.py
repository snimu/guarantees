from dataclasses import dataclass
from typing import Union, List

from guarantees.parameter_guarantees.signals.base import Signal


@dataclass
class SignalMinGEMax(Signal):
    guarantee_type_name: str   # The type of the signal
    minimum: Union[int, float, complex]
    maximum: Union[int, float, complex]


@dataclass
class SignalMinReGEMaxRe(SignalMinGEMax):
    pass


@dataclass
class SignalMinImGEMaxIm(SignalMinGEMax):
    pass


@dataclass
class SignalMinViolated(Signal):
    guarantee_type_name: str
    arg: Union[int, float, complex]
    minimum: Union[int, float, complex]


@dataclass
class SignalMinReViolated(SignalMinViolated):
    pass


@dataclass
class SignalMinImViolated(SignalMinViolated):
    pass


@dataclass
class SignalMaxViolated(Signal):
    guarantee_type_name: str
    arg: Union[int, float, complex]
    maximum: Union[int, float, complex]


@dataclass
class SignalMaxReViolated(SignalMaxViolated):
    pass


@dataclass
class SignalMaxImViolated(SignalMaxViolated):
    pass


@dataclass
class SignalNotIn(Signal):
    guarantee_type_name: str
    arg: Union[int, float, complex]
    isin: List
