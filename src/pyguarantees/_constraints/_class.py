from dataclasses import dataclass
from typing import Type

from ._base import _TypeGuarantee
from pyguarantees._constraints._util.error_handeling import \
    handle_error
from pyguarantees._constraints._util.typenames import \
    get_arg_type_name
from pyguarantees._constraints._util.common_checks import \
    enforce_dynamic_checks, check_forbidden_values


@dataclass
class _IsClass(_TypeGuarantee):
    class_type: Type = None

    def __post_init__(self):
        self.guarantee_name = "IsClass"
        self.guaranteed_type = self.class_type

    def enforce(self, arg):
        arg = _check_isclass(arg, self)
        arg = check_forbidden_values(arg, self)
        enforce_dynamic_checks(arg, self)
        return arg


def _check_isclass(arg: object, guarantee: _IsClass) -> object:
    if guarantee.class_type is None or isinstance(arg, guarantee.class_type):
        return arg

    handle_error(
        where=guarantee.where,
        type_or_value="type",
        guarantee=guarantee,
        parameter_name=guarantee.parameter_name,
        what_dict={
            "should_type": str(guarantee.class_type),
            "actual_type": get_arg_type_name(arg)
        }
    )
