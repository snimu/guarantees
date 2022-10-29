from typing import List, Tuple, Dict, Any
import inspect

from guarantees.functional_guarantees.classes import Guarantee, NoOp
from guarantees.functional_guarantees.classes.util.typenames import \
    get_arg_type_name
from guarantees.functional_guarantees.classes.util.error_handeling import \
    handle_error


class ParameterHandler:
    """
    Since it is possible to call functions and methods with a mixture of
    args and kwargs (and a different mixture at different calls!), and kwargs
    can be used in any order, figuring out which kwarg is given which guarantees
    from the function call + guarantees-ordering alone is impossible.

    Instead, a dict has to be created with an entry for every function and
    method. For each fct, all classes will be entered into an args-list
    responsible for handling args (the order is determined by the order in
    which the classes appear in the list given to @guarantees.functional_guarantees()),
    and a kwargs-dict responsible for handling kwargs (where the key is the
    name given to the guarantees  ->  the parameter-names and guarantees-names
    must match for this library to handle keyword arguments!
    """
    handles = {}

    @classmethod
    def contains(cls, fct):
        if fct in cls.handles.keys():
            return True
        return False


class ReturnHandler:
    handles = {}

    @classmethod
    def contains(cls, fct):
        if fct in cls.handles.keys():
            return True
        return False


def register_parameter_guarantees(
        fct,
        param_guarantees: List[Guarantee]):
    """Register the classes for the function."""
    if fct in ParameterHandler.handles.keys():
        # only need to register once
        #   -> when more than one call to @guarantees.functional_guarantees
        #   is made on the same function / method, only the first will be used
        #   and the rest will be ignored.
        return

    module, qualname = _get_module_qualname(fct)

    if type(param_guarantees) is not list \
            and not all(isinstance(g, Guarantee) for g in param_guarantees):
        handle_error(
            where="internal",
            type_or_value="type",
            guarantee=None,
            parameter_name="@guarantees.functional_guarantees.add_guarantees: "
                           "param_guarantees",
            what_dict={
                "should_type": "List[Guarantee]",
                "actual_type": f"{get_arg_type_name(param_guarantees)}"
            }
        )

    # Raise exception if duplicate names exist
    _check_duplicate_names(param_guarantees)

    # Prepare the handles
    ParameterHandler.handles[fct] = {"args": [], "kwargs": {}}

    for param_guarantee in param_guarantees:
        param_guarantee.qualname = qualname
        param_guarantee.module = module
        param_guarantee.where = "parameter"

        ParameterHandler.handles[fct]["args"].append(param_guarantee)
        ParameterHandler.handles[fct]["kwargs"][param_guarantee.parameter_name] = param_guarantee


def register_return_guarantees(
        fct,
        return_guarantee: Guarantee):
    if fct in ReturnHandler.handles.keys():
        return

    module, qualname = _get_module_qualname(fct)

    return_guarantee.qualname = qualname
    return_guarantee.module = module
    return_guarantee.where = "return"
    ReturnHandler.handles[fct] = return_guarantee


def _get_module_qualname(fct) -> Tuple[str, str]:
    members = inspect.getmembers(fct)

    module = ""
    qualname = ""

    for member in members:
        if member[0] == "__qualname__":
            qualname = member[1]
            continue
        if member[0] == "__module__":
            module = member[1]

    return module, qualname


def _check_duplicate_names(value_guarantees):
    names = []
    for param_guarantee in value_guarantees:
        if param_guarantee.parameter_name in names:
            handle_error(
                where="internal",
                type_or_value="value",
                guarantee=param_guarantee,
                parameter_name=f"{param_guarantee.guarantee_name}.name",
                what_dict={
                    "error": f"duplicate parameter name "
                             f"'{param_guarantee.parameter_name}'"
                }
            )

        names.append(param_guarantee.parameter_name)


def enforce_parameter_guarantees(
        fct,
        *args,
        **kwargs
) -> Tuple[Tuple, Dict]:
    # Since the args and kwargs are potentially changed,
    # create a list and dict for returning the (changed)
    # args and kwargs.
    return_args = []
    return_kwargs = {}

    # zip ensures that this only checks the args, and in the correct order
    for param_guarantee, arg in zip(ParameterHandler.handles[fct]["args"], args):
        return_args.append(_enforce_val(arg, param_guarantee))

    # Python classes that the kwargs contain no duplicates of the args
    for key, val in kwargs.items():
        return_kwargs[key] = \
            _enforce_val(val, ParameterHandler.handles[fct]["kwargs"][key])

    return tuple(return_args), return_kwargs


def enforce_return_guarantees(fct, val) -> Any:
    return _enforce_val(val, ReturnHandler.handles[fct])


def _enforce_val(val, param_guarantee: Guarantee):
    """Enforce the classes on a single value."""
    if not isinstance(param_guarantee, Guarantee):
        raise TypeError("Parameter guarantees is not a Guarantee. "
                        "@functional_guarantees only takes Guarantees.")

    if isinstance(param_guarantee, NoOp):
        return val

    return param_guarantee.enforce(val)

