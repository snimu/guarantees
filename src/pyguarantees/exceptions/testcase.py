from pyguarantees.testcase import fdata


class TestsNotImplementedError(Exception):
    """Test for a function was guaranteed but not implemented."""
    def __init__(self, functions):
        self.functions = functions
        self.description = "\n\n\tNo tests were implemented for the following " \
                           "objects: \n\n" + _where_str(functions, "no test")
        super().__init__(self.description)


class NotUsedInTestsError(Exception):
    """A test for a function was guaranteed and implemented, but the
    function was never called."""
    def __init__(self, functions):
        self.functions = functions
        self.description = "\n\n\tThe following objects were not " \
                           "used in their assigned tests: \n\n" \
                           + _where_str(functions, "unused")

        super().__init__(self.description)


def _where_str(functions: callable, why: str) -> str:
    where: str = ""

    for i, fct in enumerate(functions):
        if why == "no test":
            where += _where_str_no_test(i, fct)
        elif why == "unused":
            where += _where_str_unused(i, fct)

    return where


def _where_str_no_test(i, fct):
    where = f"\t{i + 1}. " f"Missing test-case for the following callable: \n"
    where += f"\t\tName: \t\t{fct.__qualname__}\n"
    where += f"\t\tModule: \t{fct.__module__}\n"
    return where


def _where_str_unused(i, fct):
    where = f"\t{i + 1}. " \
            f"The following callable was not called " \
            f"in its assigned tests: \n"
    where += f"\t\tName: \t\t{fct.__qualname__}\n"
    where += f"\t\tModule: \t{fct.__module__}\n"
    where += "\t\tThis callable is tested but not called " \
             "in the following test-cases: \n"

    for tfct in fdata.get(fct).get("testcases_without_exec"):
        where += f"\t\t\t\t\t- Name: \t{tfct.__qualname__}\n"
        where += f"\t\t\t\t\t   Module: \t{tfct.__module__}\n"

    return where