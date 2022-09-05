from ._exceptions import FunctionNotUsedError, TestNotImplementedError


def guarantee_test_for(fct_name, /, *, namespace="", guarantee_use=False):
    # TODO (snimu)
    #   - register guarantee
    #       - including guarantee_use
    #   - if guarantee_use: increment counter in data

    def _fct(fct):
        return fct

    return _fct


def implements_test_for(fct_name, /, *, namespace=""):
    # TODO (snimu)
    #   - signal that fct was used
    #   - if guarantee_use: check if fct was used and then reset counter

    pass
