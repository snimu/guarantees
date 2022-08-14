"""Defines the @guarantees.parameter_guarantees decorator."""


from ._guarantee_handler import enforce_guarantees, register_guarantees, Handler


def parameter_guarantees(param_guarantees, /):
    """

    :param param_guarantees:
    :return:
    """
    def _fct(fct):
        if not Handler.contains(fct):
            register_guarantees(fct, param_guarantees)

        def _enforce(*args, **kwargs):
            args, kwargs = enforce_guarantees(fct, *args, **kwargs)
            return fct(*args, **kwargs)

        return _enforce
    return _fct


