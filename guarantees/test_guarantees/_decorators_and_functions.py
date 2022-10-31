fdata = {}   # all necessary data on guaranteed functions


def guarantee_test_for(fct, /):
    global fdata
    if fct in fdata.keys():
        return

    fdata[fct] = {
        "has_test": False,
        "counter": 0,
        "was_called": True,
        "use_guaranteed": False
    }


def enforce():
    pass


def guarantee_usage(fct, /):
    global fdata
    if fct not in fdata.keys():
        return fct

    if not fdata[fct]["use_guaranteed"]:
        fdata[fct]["use_guaranteed"] = True

    # To allow comparison of counter before and after test
    #   -> if increased, fct was called
    fdata[fct]["counter"] += 1

    return fct


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
