import inspect


class TestsNotImplementedError(Exception):
    """Test for a function was guaranteed but not implemented."""
    def __init__(self, functions):
        self.functions = functions
        self.err_str = "\n\n\tNo tests were implemented for the following " \
                       "methods and functions: \n\n" + _where_str(functions)
        super().__init__(self.err_str)


class NotUsedInTestsError(Exception):
    """A test for a function was guaranteed and implemented, but the
    function was never called."""
    def __init__(self, functions):
        self.functions = functions
        self.err_str = "\n\n\tThe following methods and functions were not " \
                       "executed in their assigned tests: \n\n" \
                       + _where_str(functions)

        super().__init__(self.err_str)


def _where_str(functions: callable) -> str:
    where_str = ""

    for i, fct in enumerate(functions):
        ftype = "method" if inspect.ismethod(fct) else "function"
        where_str = f"\t{i + 1}. {ftype}\n"

        qualname, module = _get_qualname_and_module(fct)

        where_str += f"\t\tName: \t{qualname}\n"
        where_str += f"\t\tModule: \t{module}"

    return where_str


def _get_qualname_and_module(fct):
    members = inspect.getmembers(fct)

    qualname = ""
    module = ""

    for member in members:
        if member[0] == "__qualname__":
            qualname = member[1]
        elif member[1] == "__module__":
            module = member[1]

    return qualname, module



