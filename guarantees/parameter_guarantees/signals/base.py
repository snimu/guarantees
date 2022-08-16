from dataclasses import dataclass


@dataclass
class Signal:
    parameter_name: str


@dataclass
class SignalTypeError(Signal):
    guarantee_type_name: str
    should_type_name: str
    is_type_name: str
    force_conversion: bool = False
