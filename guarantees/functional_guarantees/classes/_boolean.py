from dataclasses import dataclass

from ._base import TypeGuarantee
from guarantees.functional_guarantees.classes.util.common_checks import \
    enforce_check_functions, check_type


@dataclass
class IsBool(TypeGuarantee):
    guarantee_name = "IsBool"
    guaranteed_type = bool

    def enforce(self, arg):
        arg = check_type(arg, self)
        enforce_check_functions(arg, self)
        return arg
