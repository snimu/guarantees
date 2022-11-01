import copy
from ._wrapper import Wrapper


def guarantee_test(guarantee_usage: bool = False):
    def _fct(fct):
        return Wrapper(fct, guarantee_usage)
    return _fct


def implements_test_for(guaranteed_fct: Wrapper, /):
    guaranteed_fct.has_test = True

    def _fct(test_fct):
        def _execute(*args, **kwargs):
            counter_old = copy.copy(guaranteed_fct.counter)
            ret_val = test_fct(*args, **kwargs)

            if guaranteed_fct.guarantee_usage:
                if counter_old == guaranteed_fct.counter:
                    # fct was not called (calling would have increased counter)
                    guaranteed_fct.was_called = False

            return ret_val

        return _execute

    return _fct


"""
fdata = {}   # all necessary data on guaranteed functions


def guarantee_test_for(fct, /):
    global fdata
    if fct not in fdata.keys():
        fdata[fct] = {
            "has_test": False,
            "counter": 0,
            "was_called": True,
            "use_guaranteed": False
        }


def guarantee_usage(fct, /):
    global fdata
    if fct not in fdata.keys():
        return

    fdata[fct]["use_guaranteed"] = True
    fdata[fct]["counter"] += 1

    return fct


def enforce():
    pass


def implements_test_for(guaranteed_fct, /):
    global fdata
    fdata[guaranteed_fct]["has_test"] = True

    def _fct(test_fct):
        def _execute(*args, **kwargs):
            counter_old = fdata[guaranteed_fct]["counter"]
            ret_val = test_fct(*args, **kwargs)

            if fdata[guaranteed_fct]["use_guaranteed"]:
                counter_new = fdata[guaranteed_fct]["counter"]

                if counter_old == counter_new:
                    # fct was not called (calling would have increased counter)
                    fdata[guaranteed_fct]["was_called"] = False

            return ret_val

        return _execute

    return _fct
"""
