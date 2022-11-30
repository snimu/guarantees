import copy
from functools import wraps
import warnings


fdata = {}   # all necessary data on guaranteed functions


def guarantee_test():
    def _fct(fct):
        global fdata
        if fct not in fdata.keys():
            fdata[fct] = {
                "num_tests": 0,
                "call_counter": 0,
                "usage_guaranteed": False,
                "testcases_without_exec": None
            }

        return fct
    return _fct


def guarantee_usage():
    def _fct(fct):
        global fdata

        @wraps(fct)
        def _run(*args, **kwargs):
            if _run in fdata.keys():
                fdata[_run]["call_counter"] += 1
            return fct(*args, **kwargs)

        if _run not in fdata.keys():
            fdata[_run] = {
                "num_tests": 0,
                "call_counter": 0,
                "num_tests_with_calls": 0,
                "usage_guaranteed": True,
                "testcases_without_exec": None
            }
        return _run
    return _fct


def implements_test_for(*functions, **kwfunctions):
    global fdata

    functions = list(functions)
    functions.extend(kwfunctions.values())

    # Only handle functions and methods
    #  that have a @guarantee_test decorator.
    tmp_functions = []
    for function in functions:
        if function in fdata.keys():
            tmp_functions.append(function)
        else:
            warnings.warn(
                f"The following function was given to implements_test_for "
                f"but was not decorated with @guarantee_test: "
                f" {function.__qualname__}")
    functions = tmp_functions

    for function in functions:
        fdata[function]["num_tests"] += 1

    def _fct(test_fct):
        def _run(*args, **kwargs):
            counts_old = [copy.copy(fdata[fct]["call_counter"]) for fct in functions]
            ret_val = test_fct(*args, **kwargs)

            counts_new = [copy.copy(fdata[fct]["call_counter"]) for fct in functions]

            for i, fct in enumerate(functions):
                if counts_new[i] <= counts_old[i]:
                    if fdata[fct]["testcases_without_exec"] is None:
                        fdata[fct]["testcases_without_exec"] = [test_fct]
                    else:
                        fdata[fct]["testcases_without_exec"].append(test_fct)

            return ret_val

        return _run

    return _fct
