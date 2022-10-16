from typing import List, Tuple, Dict, Any, Union

from guarantees.functional_guarantees.classes import Guarantee, IsInt, IsFloat, \
    IsComplex, IsBool, IsDict, IsSet, IsFrozenSet, IsStr, IsList, IsRange, \
    IsTuple, IsClass, IsBytes, IsByteArray, IsMemoryView, NoOp, IsNone, IsUnion
from guarantees.functional_guarantees.enforcement.util.typenames import \
    get_guaranteed_type_name, get_type_name, get_guaranteed_type, \
    get_guarantee_name
from guarantees.functional_guarantees.enforcement.util.error_handeling import \
    handle_error
from guarantees.functional_guarantees.enforcement.util.common_checks import \
    enforce_check_functions

from ._enforce_numeric import enforce_isint, enforce_isfloat, \
     enforce_iscomplex
from ._enforce_string import enforce_isstr
from ._enforce_boolean import enforce_isbool
from ._enforce_collections import enforce_islist, enforce_istuple, \
    enforce_isdict, enforce_isset, enforce_isfrozenset, enforce_isrange
from ._enforce_other import enforce_isclass, enforce_isnone
from ._enforce_binary import enforce_isbytes, enforce_isbytearray, \
    enforce_ismemoryview


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
        function_name: str,
        function_namespace: str,
        param_guarantees: List[Guarantee]):
    """Register the classes for the function."""
    if fct in ParameterHandler.handles.keys():
        # only need to register once
        #   -> when more than one call to @guarantees.functional_guarantees
        #   is made on the same function / method, only the first will be used
        #   and the rest will be ignored.
        return

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
                "actual_type": f"{get_type_name(param_guarantees)}"
            }
        )

    # Raise exception if duplicate names exist
    _check_duplicate_names(param_guarantees)

    # Prepare the handles
    ParameterHandler.handles[fct] = {"args": [], "kwargs": {}}

    for param_guarantee in param_guarantees:
        param_guarantee.function_name = function_name
        param_guarantee.function_namespace = function_namespace
        param_guarantee.where = "parameter"

        ParameterHandler.handles[fct]["args"].append(param_guarantee)
        ParameterHandler.handles[fct]["kwargs"][param_guarantee.parameter_name] = param_guarantee


def register_return_guarantees(
        fct,
        function_name,
        function_namespace,
        return_guarantee: Guarantee):
    if fct in ReturnHandler.handles.keys():
        return

    return_guarantee.function_name = function_name
    return_guarantee.function_namespace = function_namespace
    return_guarantee.where = "return"
    ReturnHandler.handles[fct] = return_guarantee


def _check_duplicate_names(value_guarantees):
    names = []
    for param_guarantee in value_guarantees:
        if param_guarantee.parameter_name in names:
            handle_error(
                where="internal",
                type_or_value="value",
                guarantee=param_guarantee,
                parameter_name=f"{get_guarantee_name(param_guarantee)}.name",
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


def _enforce_isunion(arg: Any, param_guarantee: IsUnion) -> Any:
    """`enforce_isunion` cannot make use of other `enforce_...`-fcts
    without a circular import -> must be defined here."""
    if arg is None:
        return arg

    enforce_check_functions(arg, param_guarantee)

    for guarantee in param_guarantee.guarantees:
        guarantee.function_name = f"{param_guarantee.function_name}: IsUnion"
        guarantee.function_namespace = param_guarantee.function_namespace

        # 1. Try to change arg to wanted type if allowed
        # 1.1  If ValueError: definitely wrong type -> continue
        # 2. Check type (whether force_conversion or not)
        # 2.1  If wrong type: loop continues or type is false
        # 2.2  If right type: enforce it
        if guarantee.force_conversion:
            try:
                target_type = get_guaranteed_type(guarantee)
                if isinstance(guarantee, IsClass):
                    target_type = guarantee.class_type
                arg = target_type(arg)
            except ValueError:
                continue

        target_type = get_guaranteed_type(guarantee)
        if isinstance(guarantee, IsClass):
            target_type = guarantee.class_type
        if type(arg) is target_type:
            return _enforce_val(arg, guarantee)

    # Didn't work
    should_types = \
        [get_guaranteed_type_name(g) for g in param_guarantee.guarantees]
    handle_error(
        where=param_guarantee.where,
        type_or_value="type",
        guarantee=param_guarantee,
        parameter_name=param_guarantee.parameter_name,
        what_dict={
            "should_type": f"Union{should_types}",
            "actual_type": get_type_name(arg)
        }
    )

    # In case of warnings_only
    return arg


guarantee_enforcer_mapping = {
    IsInt: enforce_isint,
    IsFloat: enforce_isfloat,
    IsComplex: enforce_iscomplex,
    IsStr: enforce_isstr,
    IsBool: enforce_isbool,
    IsClass: enforce_isclass,
    IsList: enforce_islist,
    IsTuple: enforce_istuple,
    IsDict: enforce_isdict,
    IsSet: enforce_isset,
    IsFrozenSet: enforce_isfrozenset,
    IsRange: enforce_isrange,
    IsNone: enforce_isnone,
    IsUnion: _enforce_isunion,
    IsBytes: enforce_isbytes,
    IsByteArray: enforce_isbytearray,
    IsMemoryView: enforce_ismemoryview
}


def _enforce_val(val, param_guarantee: Guarantee):
    """Enforce the classes on a single value."""
    if not isinstance(param_guarantee, Guarantee):
        raise TypeError("Parameter guarantees is not a Guarantee. "
                        "@functional_guarantees only takes Guarantees.")

    if isinstance(param_guarantee, NoOp):
        return val

    global guarantee_enforcer_mapping
    enforce_fct = guarantee_enforcer_mapping[type(param_guarantee)]
    return enforce_fct(val, param_guarantee)

