from typing import List, Tuple, Dict

from guarantees.parameter_guarantees.classes import Guarantee, IsInt, IsFloat, \
    IsComplex, IsBool, IsDict, IsSet, IsFrozenSet, IsStr, IsList, IsRange, \
    IsTuple, IsClass, IsBytes, IsByteArray, IsMemoryView, NoOp, IsNone

from ._enforce_numeric import enforce_isint, enforce_isfloat, \
     enforce_iscomplex
from ._enforce_string import enforce_isstr
from ._enforce_boolean import enforce_isbool
from ._enforce_collections import enforce_islist, enforce_istuple, \
    enforce_isdict, enforce_isset, enforce_isfrozenset, enforce_isrange
from ._enforce_other import enforce_isclass, enforce_isnone


class Handler:
    """
    Since it is possible to call functions and methods with a mixture of
    args and kwargs (and a different mixture at different calls!), and kwargs
    can be used in any order, figuring out which kwarg is given which guarantees
    from the function call + guarantees-ordering alone is impossible.

    Instead, a dict has to be created with an entry for every function and
    method. For each fct, all classes will be entered into an args-list
    responsible for handling args (the order is determined by the order in
    which the classes appear in the list given to @guarantees.parameter_guarantees()),
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


def register_guarantees(fct, param_guarantees: List[Guarantee]):
    """Register the classes for the function."""
    if fct in Handler.handles.keys():
        # only need to register once
        #   -> when more than one call to @guarantees.parameter_guarantees is made
        #   on the same function / method, only the first will be used
        #   and the rest will be ignored.
        return

    if type(param_guarantees) is not list \
            and not all(isinstance(g, Guarantee) for g in param_guarantees):
        raise ValueError("@guarantees.parameter_guarantees takes "
                         "a list of classes! "
                         f"You have given it: {type(param_guarantees)}")

    # Raise exception if duplicate names exist
    _check_duplicate_names(param_guarantees)

    # Prepare the handles
    Handler.handles[fct] = {"args": [], "kwargs": {}}

    for param_guarantee in param_guarantees:
        Handler.handles[fct]["args"].append(param_guarantee)
        Handler.handles[fct]["kwargs"][param_guarantee.parameter_name] = param_guarantee


def _check_duplicate_names(param_guarantees):
    names = []
    for param_guarantee in param_guarantees:
        if param_guarantee.parameter_name in names:
            raise ValueError("@guarantees.parameter_guarantees: "
                             "Duplicate guarantees name: "
                             f"'{param_guarantee.parameter_name}'")
        names.append(param_guarantee.parameter_name)


def enforce_guarantees(
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
    for param_guarantee, arg in zip(Handler.handles[fct]["args"], args):
        return_args.append(_enforce_arg(arg, param_guarantee))

    # Python classes that the kwargs contain no duplicates of the args
    for key, val in kwargs.items():
        return_kwargs[key] = \
            _enforce_arg(val, Handler.handles[fct]["kwargs"][key])

    return tuple(return_args), return_kwargs


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
    IsNone: enforce_isnone
}


def _enforce_arg(arg, param_guarantee: Guarantee):
    """Enforce the classes on a single argument."""
    if not isinstance(param_guarantee, Guarantee):
        raise TypeError("Parameter guarantees is not a Guarantee. "
                        "@parameter_guarantees only takes Guarantees.")
    
    if isinstance(param_guarantee, NoOp):
        return arg

    global guarantee_enforcer_mapping
    enforce_fct = guarantee_enforcer_mapping[type(param_guarantee)]
    return enforce_fct(arg, param_guarantee)

