from typing import List, Tuple, Dict

from guarantee.type_guarantees.guarantees import Guarantee, IsInt, IsFloat, \
    IsComplex, IsBool, IsDict, IsSet, IsFrozenSet, IsStr, IsList, IsRange, \
    IsTuple, IsClass, IsBytes, IsByteArray, IsMemoryView, NoOp

from ._enforce_numeric import enforce_isint, enforce_isfloat, \
     enforce_iscomplex
from ._enforce_string import enforce_isstr
from ._enforce_boolean import enforce_isbool
from ._enforce_collections import enforce_islist, enforce_istuple, \
    enforce_isdict, enforce_isset, enforce_isfrozenset
from ._enforce_other import enforce_isclass


class Handler:
    """
    Since it is possible to call functions and methods with a mixture of
    args and kwargs (and a different mixture at different calls!), and kwargs
    can be used in any order, figuring out which kwarg is given which guarantee
    from the function call + guarantee-ordering alone is impossible.

    Instead, a dict has to be created with an entry for every function and
    method. For each fct, all guarantees will be entered into an args-list
    responsible for handling args (the order is determined by the order in
    which the guarantees appear in the list given to @guarantee.type_guarantees()),
    and a kwargs-dict responsible for handling kwargs (where the key is the
    name given to the guarantee  ->  the parameter-names and guarantee-names
    must match for this library to handle keyword arguments!
    """
    handles = {}

    @classmethod
    def contains(cls, fct):
        if fct in cls.handles.keys():
            return True
        return False


def register_guarantees(fct, param_guarantees: List[Guarantee]):
    """Register the guarantees for the function."""
    if fct in Handler.handles.keys():
        # only need to register once
        #   -> when more than one call to @guarantee.type_guarantees is made
        #   on the same function / method, only the first will be used
        #   and the rest will be ignored.
        return

    if type(param_guarantees) is not list \
            and not all(isinstance(g, Guarantee) for g in param_guarantees):
        raise ValueError("@guarantee.type_guarantees takes "
                         "a list of guarantees! "
                         f"You have given it: {type(param_guarantees)}")

    # Raise exception if duplicate names exist
    _check_duplicate_names(param_guarantees)

    # Prepare the handles
    Handler.handles[fct] = {"args": [], "kwargs": {}}

    for param_guarantee in param_guarantees:
        Handler.handles[fct]["args"].append(param_guarantee)
        Handler.handles[fct]["kwargs"][param_guarantee.name] = param_guarantee


def _check_duplicate_names(param_guarantees):
    names = []
    for param_guarantee in param_guarantees:
        if param_guarantee.name in names:
            raise ValueError("@guarantee.type_guarantees: "
                             "Duplicate guarantee name: "
                             f"'{param_guarantee.name}'")
        names.append(param_guarantee.name)


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

    # Python guarantees that the kwargs contain no duplicates of the args
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
    IsFrozenSet: enforce_isfrozenset
}


def _enforce_arg(arg, param_guarantee: Guarantee):
    """Enforce the guarantees on a single argument."""
    if not isinstance(param_guarantee, Guarantee):
        raise TypeError("Parameter guarantee is not a Guarantee. "
                        "@parameter_guarantees only takes Guarantees.")
    
    if isinstance(param_guarantee, NoOp):
        return arg

    global guarantee_enforcer_mapping
    enforce_fct = guarantee_enforcer_mapping[type(param_guarantee)]
    return enforce_fct(arg, param_guarantee)

