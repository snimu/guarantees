class TestNotImplementedError(Exception):
    """A test for a function was guaranteed but not implemented."""
    pass


class FunctionNotUsedError(Exception):
    """A test for a function was guaranteed and implemented, but the
    function was never called."""
    pass
