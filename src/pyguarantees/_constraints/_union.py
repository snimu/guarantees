from dataclasses import dataclass
from typing import List, Union

from ._base import _TypeGuarantee
from ._no_op import _NoOp
from pyguarantees._constraints._util.error_handeling import \
    handle_error
from pyguarantees._constraints._util.typenames import \
    get_arg_type_name, get_type_name
from pyguarantees._constraints._util.common_checks import \
    enforce_dynamic_checks, check_forbidden_values


@dataclass
class _IsUnion(_TypeGuarantee):
    guarantees: List[_TypeGuarantee] = None

    def __post_init__(self):
        self.guarantee_name = "IsUnion"
        self.guaranteed_type = Union

    def enforce(self, arg):
        arg = self.__enforce_union_guarantees(arg)
        arg = check_forbidden_values(arg, self)
        enforce_dynamic_checks(arg, self)
        return arg

    def __enforce_union_guarantees(self, arg):
        for guarantee in self.guarantees:
            self.__handle_noop(guarantee)
            self.__handle_isunion(guarantee)

            guarantee.qualname = f"{self.qualname}: IsUnion"
            guarantee.module = self.module

            # 1. Try to change arg to wanted type if allowed
            # 1.1  If ValueError: definitely wrong type -> continue
            # 2. Check type (whether force_conversion or not)
            # 2.1  If wrong type: loop continues or type is false
            # 2.2  If right type: enforce it

            # Different type-check for None
            if arg is guarantee.guaranteed_type is None:
                return guarantee.enforce(arg)
            elif guarantee.guaranteed_type is None:
                continue   # no conversion attempt necessary; arg should be None but isn't
            elif arg is None:
                continue   # arg should not be None but is

            # Attempt conversion
            if guarantee.force_conversion:
                try:
                    arg = guarantee.guaranteed_type(arg)   # might be int or float -> int(arg) or float(arg)
                except ValueError:
                    continue

            if type(arg) is guarantee.guaranteed_type:
                return guarantee.enforce(arg)

        # Didn't work
        should_types = \
            [get_type_name(g.guaranteed_type) for g in self.guarantees]
        handle_error(
            where=self.where,
            type_or_value="type",
            guarantee=self,
            parameter_name=self.parameter_name,
            what_dict={
                "should_type": f"Union{should_types}",
                "actual_type": get_arg_type_name(arg)
            }
        )

        # In case of warnings_only
        return arg

    def __handle_noop(self, guarantee):
        if not isinstance(guarantee, _NoOp):
            return

        handle_error(
            where="internal",
            type_or_value="type",
            guarantee=self,
            parameter_name=self.parameter_name,
            what_dict={"error": "IsUnion may not contain NoOp."}
        )

    def __handle_isunion(self, guarantee):
        if not isinstance(guarantee, _IsUnion):
            return

        handle_error(
            where="internal",
            type_or_value="type",
            guarantee=self,
            parameter_name=self.parameter_name,
            what_dict={"error": "IsUnion may not contain IsUnion."}
        )
