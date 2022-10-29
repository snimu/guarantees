import inspect


# TODO (snimu): this returns True for staticmethods; however, I only want
#   it to return True for bound methods
#   -> create isboundmethod(fct) which calls ismethod as well as some other
#   -> distinguishing criterion between staticmethod and other methods
def ismethod(fct) -> bool:
    """
    The `inspect.ismethod` function doesn't work on a method when called
     from inside the decorator of that method; it always returns `False`.

    Instead, use the `inspect.getmembers` function to distinguish between
     functions and methods so that `self` and `class` can be ignored
     where appropriate.
    """
    qualname = get_qualname(fct).split(".")

    # The __qualname__ of a method is always in the form
    #   *classname*.*...*.*methodname*;
    #   Functions, on the other hand, are always in the form *functionname*
    if len(qualname) == 1:
        return False

    # Functions defined within methods are of the form
    #   *classname*.*...*.<locals>.*fname*
    if qualname[-2] == "<locals>":
        return False

    return True


def get_qualname(fct):
    members = inspect.getmembers(fct)
    for member in members:
        if member[0] != "__qualname__":
            continue

        return member[1]
