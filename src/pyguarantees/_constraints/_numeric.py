"""Includes the numeric classes float, int, and complex."""


from dataclasses import dataclass

from ._base import _TypeGuarantee
from pyguarantees._constraints._util.common_checks import (
    check_type,
    enforce_dynamic_checks,
    check_forbidden_values
)
from pyguarantees._constraints._util.numeric_checks import (
    check_min_ge_max,
    check_max,
    check_min,
    check_isin
)


@dataclass
class _NumericGuarantee(_TypeGuarantee):
    isin: list = None
    minimum: float = None
    maximum: float = None


@dataclass
class _IsInt(_NumericGuarantee):
    def __post_init__(self):
        self.guarantee_name = "IsInt"
        self.guaranteed_type = int

    def enforce(self, arg):
        arg = check_type(arg, self)
        arg = check_forbidden_values(arg, self)

        check_min_ge_max(
            guarantee=self,
            minimum=self.minimum,
            maximum=self.maximum
        )

        check_min(arg, self.minimum, self)
        check_max(arg, self.maximum, self)

        check_isin(arg, self)

        enforce_dynamic_checks(arg, self)

        return arg


@dataclass
class _IsFloat(_NumericGuarantee):
    def __post_init__(self):
        self.guarantee_name = "IsFloat"
        self.guaranteed_type = float

    def enforce(self, arg):
        arg = check_type(arg, self)
        arg = check_forbidden_values(arg, self)

        check_min_ge_max(
            guarantee=self,
            minimum=self.minimum,
            maximum=self.maximum
        )

        check_min(arg, self.minimum, self)
        check_max(arg, self.maximum, self)

        check_isin(arg, self)

        enforce_dynamic_checks(arg, self)

        return arg


@dataclass
class _IsComplex(_NumericGuarantee):
    minimum_re: float = None
    maximum_re: float = None
    minimum_im: float = None
    maximum_im: float = None

    def __post_init__(self):
        self.guarantee_name = "IsComplex"
        self.guaranteed_type = complex

    def enforce(self, arg):
        arg = check_type(arg, self)
        arg = check_forbidden_values(arg, self)

        check_min_ge_max(
            guarantee=self,
            minimum=self.minimum,
            maximum=self.maximum
        )
        check_min_ge_max(
            guarantee=self,
            minimum=self.minimum_re,
            maximum=self.maximum_re,
            minmax_type="re"
        )
        check_min_ge_max(
            guarantee=self,
            minimum=self.minimum_im,
            maximum=self.maximum_im,
            minmax_type="im"
        )

        check_min(abs(arg), self.minimum, self)
        check_max(abs(arg), self.maximum, self)
        check_min(arg.real, self.minimum_re, self, "re")
        check_max(arg.real, self.maximum_re, self, "re")
        check_min(arg.imag, self.minimum_im, self, "im")
        check_max(arg.imag, self.maximum_im, self, "im")

        check_isin(arg, self)

        enforce_dynamic_checks(arg, self)

        return arg
