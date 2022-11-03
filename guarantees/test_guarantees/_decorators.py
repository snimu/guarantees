fdata = {}   # all necessary data on guaranteed functions


def guarantee_test():
    def _fct(fct):
        global fdata
        if fct not in fdata.keys():
            fdata[fct] = {"has_test": False}

        return fct
    return _fct


def implements_test_for(guaranteed_fct, /):
    global fdata
    fdata[guaranteed_fct]["has_test"] = True

    def _fct(test_fct):
        return test_fct

    return _fct
