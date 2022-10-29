from dataclasses import dataclass

from ._base import TypeGuarantee
from guarantees.functional_guarantees.classes.util.common_checks import \
    enforce_check_functions, check_type


@dataclass
class IsBytes(TypeGuarantee):
    guarantee_name = "IsBytes"
    guaranteed_type = bytes

    def enforce(self, arg) -> bytes:
        arg = check_type(arg, self)
        enforce_check_functions(arg, self)
        return arg


@dataclass
class IsByteArray(TypeGuarantee):
    guarantee_name = "IsByteArray"
    guaranteed_type = bytearray

    def enforce(self, arg) -> bytearray:
        arg = check_type(arg, self)
        enforce_check_functions(arg, self)
        return arg


@dataclass
class IsMemoryView(TypeGuarantee):
    guarantee_name = "IsMemoryView"
    guaranteed_type = memoryview

    def enforce(self, arg) -> memoryview:
        arg = check_type(arg, self)
        enforce_check_functions(arg, self)
        return arg

