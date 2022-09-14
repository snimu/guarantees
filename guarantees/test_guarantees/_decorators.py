from .exceptions import FunctionNotUsedError, TestNotImplementedError
from ._data import TestGuarantees


def guarantee_test_for(name, /, *, namespace=None, guarantee_use=False):
    def _fct(fct):
        if not TestGuarantees.contains(name, namespace):
            TestGuarantees.register_for_testing(
                name,
                namespace,
                fct if guarantee_use else None
            )

        if guarantee_use:
            TestGuarantees.increment_counter(name, namespace)

        return fct
    return _fct


def implements_test_for(name, /, *, namespace=""):
    TestGuarantees.signal_has_test(name, namespace)

    def _fct(fct):
        def _execute(*args, **kwargs):
            counter_old = TestGuarantees.get_counter(name, namespace)
            ret_val = fct(*args, **kwargs)

            if TestGuarantees.use_guaranteed(name, namespace):
                counter_new = TestGuarantees.get_counter(name, namespace)

                if counter_old == counter_new:
                    # fct was not called (calling would have increased counter)
                    TestGuarantees.set_was_called_false(name, namespace)

            return ret_val
        return _execute
    return _fct
