import inspect

from ._decorators import fdata


class TestsNotImplementedError(Exception):
    """Test for a function was guaranteed but not implemented."""
    def __init__(self, functions):
        self.functions = functions
        self.err_str = "\n\n\tNo tests were implemented for the following " \
                       "methods and functions: \n\n" + _where_str(functions)
        super().__init__(self.err_str, "no test")


class NotUsedInTestsError(Exception):
    """A test for a function was guaranteed and implemented, but the
    function was never called."""
    def __init__(self, functions):
        self.functions = functions
        self.err_str = "\n\n\tThe following methods and functions were not " \
                       "executed in their assigned tests: \n\n" \
                       + _where_str(functions, "unused")

        super().__init__(self.err_str)


def _where_str(functions: callable, why: str) -> str:
    where_str = ""

    for i, fct in enumerate(functions):
        if why == "no test":
            where_str += f"\t{i + 1}. " \
                         f"Missing test-case for the following callable: \n"
        elif why == "unused":
            where_str += f"\t{i + 1}. " \
                         f"The following callable was not called " \
                         f"in its assigned tests: \n"

        qualname, module = fdata[fct]["info"].qualname, fdata[fct]["info"].module

        where_str += f"\t\tName: \t\t{qualname}\n"
        where_str += f"\t\tModule: \t{module}\n"

        if why == "unused":
            where_str += "\t\tThis callable is tested but not called " \
                         "in the following test-cases: \n"

            for tinfo in fdata[fct]["testcases_without_exec"]:
                where_str += f"\t\t\t\t\t- Name: \t{tinfo.qualname}\n"
                where_str += f"\t\t\t\t\t   Module: \t{tinfo.module}\n"

    return where_str
