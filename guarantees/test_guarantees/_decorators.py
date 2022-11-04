from typing import Union, List
import copy
import inspect
from dataclasses import dataclass


fdata = {}   # all necessary data on guaranteed functions


def _get_qualname_and_module(fct):
    members = inspect.getmembers(fct)

    qualname = ""
    module = ""
    for member in members:
        if member[0] == "__qualname__":
            qualname = member[1]
        elif member[0] == "__module__":
            module = member[1]

    return qualname, module


@dataclass
class Info:
    qualname: str
    module: str


def guarantee_test():
    def _fct(fct):
        global fdata
        if fct not in fdata.keys():
            qualname, module = _get_qualname_and_module(fct)
            fdata[fct] = {
                "num_tests": 0,
                "call_counter": 0,
                "usage_guaranteed": False,
                "info": Info(qualname, module),
                "testcases_without_exec": None
            }

        return fct
    return _fct


def guarantee_usage():
    def _fct(fct):
        def _run(*args, **kwargs):
            global fdata
            if _run in fdata.keys():
                fdata[_run]["call_counter"] += 1
            return fct(*args, **kwargs)

        if _run not in fdata.keys():
            qualname, module = _get_qualname_and_module(fct)
            fdata[_run] = {
                "num_tests": 0,
                "call_counter": 0,
                "num_tests_with_calls": 0,
                "usage_guaranteed": True,
                "info": Info(qualname, module),
                "testcases_without_exec": None
            }
        return _run
    return _fct


def implements_test_for(functions: Union[callable, List[callable]], /):
    global fdata

    if callable(functions):
        functions = [functions]

    for function in functions:
        fdata[function]["num_tests"] += 1

    def _fct(test_fct):
        def _run(*args, **kwargs):
            counts_old = [copy.copy(fdata[fct]["call_counter"]) for fct in functions]
            ret_val = test_fct(*args, **kwargs)

            counts_new = [copy.copy(fdata[fct]["call_counter"]) for fct in functions]

            for i, fct in enumerate(functions):
                if counts_new[i] <= counts_old[i]:
                    info = Info(*_get_qualname_and_module(test_fct))
                    if fdata[fct]["testcases_without_exec"] is None:
                        fdata[fct]["testcases_without_exec"] = [info]
                    else:
                        fdata[fct]["testcases_without_exec"].append(info)

            return ret_val

        return _run

    return _fct
