from typing import Union, List


fdata = {}   # all necessary data on guaranteed functions


def guarantee_test():
    def _fct(fct):
        global fdata
        if fct not in fdata.keys():
            fdata[fct] = {"has_test": False}

        return fct
    return _fct


def implements_test_for(functions: Union[callable, List[callable]], /):
    global fdata

    if callable(functions):
        functions = [functions]

    for function in functions:
        fdata[function]["has_test"] = True

    def _fct(test_fct):
        return test_fct

    return _fct
