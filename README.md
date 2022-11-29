# pyguarantees
Python: guarantee test coverage, guarantee type and runtime-guarantees.

This package has two components: `test_guarantees` and `functional_guarantees`.

# test_guarantees

`pyguarantees.test_guarantees` allows the use of decorators that guarantee the
usage of a decorated function or method in a `unittest.TestCase`. 

## Example

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

The package consists of three decorators and two functions, as well as two `Exception`s.
All are explained below.

## Decorators

The three decorators shown below cannot be used without the [functions](#functions) 
of this package.

### `guarantee_test`

Takes no arguments.

Any function or method (however nested) decorated with `guarantee_test`
that is in the scope of unittest will force unittest to throw and exception should 
it not be in an [`@implements_test_for`](#implements_test_for).

Currently, it is necessary to include the brackets &ndash; `()` &ndash; so that 
the function is registered. 

### `guarantee_usage`

Takes no arguments.

Must be used below [`@guarentee_test`](#guarantee_test), otherwise, it is ignored.

Brackets are not optional, meaning that it has to be used as 
`@guarantee_usage()`, not just `@guarantee_usage`.

Guarantees that a given function or method is used by any test-function
that is decorated by [`@implements_test_for`](#implements_test_for), if 
`@implements_test_for` takes the function or method as an argument.


### `implements_test_for`

- `args`: Give any function or method that the corresponding test is meant for.
- `kwargs`: The value will be used like an `arg`, while the key will be ignored.

Functions and methods that weren't decorated by [`@guarantee_test`](#guarantee_test) 
lead to a user-warning but are ignored otherwise.

## Functions

There are two functions. At least one has to be used for the [decorators](#decorators)
to have an effect.

### `enforce`

Takes no arguments.

Run this after running all your unittests. This runs additional unittests that 
check which functions violated their guarantees and raise [exceptions](#exceptions) 
accordingly.

It is recommended to only use this function when using a complicated unittest-setup.
When using `unittest.main()`, it is recommended to use `tg.main()` instead.

### `main`

Takes no arguments.

Calls `unittest.main()` followed by [`tg.enforce`](#enforce).

## Exceptions

There are two custom `Exception`s as presented below.

### `TestsNotImplementedError`

The `tg.exceptions.TestsNotImplementedError`.

### `NotUsedInTestsError`

The `tg.exceptions.NotUsedInTestsError`.
