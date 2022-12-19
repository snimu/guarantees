from dataclasses import dataclass
from ._base import _TypeGuarantee
from pyguarantees._constraints._util.error_handeling import handle_error
from pyguarantees._constraints._util.common_checks import enforce_dynamic_checks
from pyguarantees._constraints._util.typenames import get_arg_type_name


@dataclass
class _IsNone(_TypeGuarantee):
    def __post_init__(self):
        self.guarantee_name = "IsNone"
        self.guaranteed_type = None

    def enforce(self, arg):
        if arg is None:
            enforce_dynamic_checks(arg, self)
            return

        handle_error(
            where=self.where,
            type_or_value="type",
            guarantee=self,
            parameter_name=self.parameter_name,
            what_dict={
                "should_type": "None",
                "actual_type": get_arg_type_name(arg)
            }
        )