# guarantees
Python: guarantee test coverage, guarantee type and runtime-guarantees.

This package has two components: `test_guarantees` and `functional_guarantees`.

## test_guarantees

`pyguarantees.test_guarantees` allows the use of decorators that guarantee the
usage of a decorated function or method in a `unittest.TestCase`. This is best 
demonstrated by an example:

```python 
import unittest
from pyguarantees import test_guarantees as tg
from some_package import some_fct_with_test_guarantee
 

@tg.guarantee_test()
def foo():
    pass


@tg.guarantee_test()
@tg.guarantee_usage()
def add_one(a):
  return a + 1


class ExampleTest(unittest.TestCase):
  @implements_test_for(foo)
  def test_foo(self):
      foo()

  @implements_test_for(add_one, some_fct_with_test_guarantee)
  def test_other(self):
    val = foo(1)
    self.assertEqual(val, 2)
    
    
if __name__ == '__main__':
    tg.main()
```

All three decorators are shown in this example. They are explained in more detail below.

### `guarantee_test`

Takes no arguments.

Any function or method (however nested) decorated with `guarantee_test`
that is in the scope of unittest will force unittest to throw and exception should 
it not be in an [`implements_test_for`](#implements-test-for).

Currently, it is necessary to include the brackets &ndash; `()` &ndash; so that 
the function is registered. 

### `implements_test_for`

`args`: Give any function or method that the corresponding test is meant for.

Only 