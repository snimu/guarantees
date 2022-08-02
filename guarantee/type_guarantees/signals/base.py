from dataclasses import dataclass


@dataclass
class Signal:
    arg_name: str   # The name of the argument


@dataclass
class SignalTypeError(Signal):
    type_should: str
    type_is: str
    force_conversion: bool = False
