"""Defines the @guarantees.functional_guarantees decorator."""


from ._guarantee_handler import enforce_parameter_guarantees, \
    register_parameter_guarantees, ParameterHandler, \
    register_return_guarantees, ReturnHandler, \
    enforce_return_guarantees
from ._on_off import OnOff


def add_guarantees(
        function_name="",
        function_namespace="",
        param_guarantees=None,
        return_guarantee=None
):
    def _fct(fct):
        if not OnOff.on:
            return fct

        if not ParameterHandler.contains(fct) and param_guarantees is not None:
            register_parameter_guarantees(
                fct,
                function_name,
                function_namespace,
                param_guarantees
            )

        if not ReturnHandler.contains(fct) and return_guarantee is not None:
            register_return_guarantees(
                fct,
                function_name,
                function_namespace,
                return_guarantee
            )

        def _enforce(*args, **kwargs):
            if param_guarantees is not None:
                args, kwargs = enforce_parameter_guarantees(
                    fct, *args, **kwargs)

            ret_val = fct(*args, **kwargs)
            if return_guarantee is not None:
                ret_val = enforce_return_guarantees(fct, ret_val)
            return ret_val

        return _enforce
    return _fct