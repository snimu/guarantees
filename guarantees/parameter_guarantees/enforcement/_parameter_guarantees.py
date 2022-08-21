"""Defines the @guarantees.parameter_guarantees decorator."""


from ._guarantee_handler import enforce_guarantees, register_guarantees, Handler
from ._on_off import OnOff


def parameter_guarantees(param_guarantees, /):
    def _fct(fct):
        if not OnOff.on:
            return fct

        if not Handler.contains(fct):
            register_guarantees(fct, param_guarantees)

        def _enforce(*args, **kwargs):
            args, kwargs = enforce_guarantees(fct, *args, **kwargs)
            return fct(*args, **kwargs)

        return _enforce
    return _fct


