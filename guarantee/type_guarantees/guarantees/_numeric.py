"""Includes the numeric guarantees float, int, and complex."""


from dataclasses import dataclass
from ._base import TypeGuarantee


@dataclass
class NumericGuarantee(TypeGuarantee):
    isin: list = None
    minimum: float = None
    maximum: float = None


@dataclass
class IsFloat(NumericGuarantee):
    pass


@dataclass
class IsInt(NumericGuarantee):
    pass


@dataclass
class IsComplex(NumericGuarantee):
    minimum_re: float = None
    maximum_re: float = None
    minimum_im: float = None
    maximum_im: float = None

