# Design

## Functions

Explained by example

### File 1: function definitions
```python
from guarantees import test_guarantees as tg

# ...

# Is decorator so that it is always associated
#   with a specific function
@tg.guarantee_test_for("example_fct", namespace="path::to::file")
def example_fct():
    pass
```

Should maybe have a parameter `guarantee_use` so that
the partner decorator (see below) checks if 
the given function is actually used. 

Needs to be a decorator for that, of course. 

This would be pretty useful, but might be difficult to 
implement on the checking-side.

The `guarantee_test_for`-decorator would increment a 
counter in some external `dict`. 

The `implements_test_for`-decorator would compare that counter 
before and after calling the decorated function. 
If the counter was increased, the function was called.

### File 2: Tests

````python
import unittest
from guarantees import test_guarantees as tg
# import file 1

# ... 

class SomeTests(unittest.TestCase):
    # ...
    
    # Is decorator so that it is always associated with 
    #   an actual test function
    # Should check if it is inside a unittest TestCase
    @tg.implements_test_for("name-of-function")  
    def test_your_fct(self):
        pass   # test here
````


## Other considerations

Exceptions:

- `TestNotImplementedError`
- `FunctionNotUsedError`


