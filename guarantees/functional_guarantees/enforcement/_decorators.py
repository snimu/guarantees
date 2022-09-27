"""Defines the @guarantees.functional_guarantees decorator."""


from ._guarantee_handler import enforce_parameter_guarantees, \
    register_parameter_guarantees, ParameterHandler, \
    register_return_guarantees, ReturnHandler, \
    enforce_return_guarantees
from ._on_off import OnOff


def parameter_guarantees(param_guarantees, /):
    def _fct(fct):
        if not OnOff.on:
            return fct

        if not ParameterHandler.contains(fct):
            register_parameter_guarantees(fct, param_guarantees)

        def _enforce(*args, **kwargs):
            args, kwargs = enforce_parameter_guarantees(fct, *args, **kwargs)
            return fct(*args, **kwargs)

        return _enforce
    return _fct


def return_guarantees(return_guarantee, /):
    def _fct(fct):
        if not OnOff.on:
            return fct

        if not ReturnHandler.contains(fct):
            register_return_guarantees(fct, return_guarantee)

        def _enforce(*args, **kwargs):
            ret_val = fct(*args, **kwargs)
            return enforce_return_guarantees(fct, ret_val)

        return _enforce
    return _fct


