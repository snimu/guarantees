from dataclasses import dataclass
from typing import List

from ._base import _TypeGuarantee
from pyguarantees._constraints._util.common_checks import (
    check_type,
    enforce_dynamic_checks,
    check_forbidden_values
)
from pyguarantees._constraints._util.numeric_checks import check_isin
from pyguarantees._constraints._util.collections_checks import (
    check_minmax_len
)


@dataclass
class _IsStr(_TypeGuarantee):
    minimum_len: int = None
    maximum_len: int = None
    isin: List = None

    def __post_init__(self):
        self.guarantee_name = "IsStr"
        self.guaranteed_type = str

    def enforce(self, arg):
        arg = check_type(arg, self)
        arg = check_forbidden_values(arg, self)
        check_minmax_len(arg, self)
        check_isin(arg, self)

        enforce_dynamic_checks(arg, self)
        return arg
