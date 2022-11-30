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

As in the example, `pyguarantees.test_guarantees` will be abbreviated with `tg` from
here on out.

## Decorators

The three decorators shown below cannot be used without the [functions](#functions) 
of this package.

### `guarantee_test`

Takes no arguments.

Any function or method (however nested) decorated with `@tg.guarantee_test`
that is in the scope of unittest will force unittest to throw and exception should 
it not be in an [@tg.implements_test_for](#implements_test_for).

Currently, it is necessary to include the brackets &ndash; `()` &ndash; so that 
the function is registered. 

Having a function (or method) decorated like follows:

```python
@tg.guarantee_test()
def foo():
    pass
```

but not having a test in your `unittest.TestCase` decorated by `@implements_test_for(foo)` 
would lead to a [TestsNotImplementedError](#testsnotimplementederror) being raised.

### `guarantee_usage`

Takes no arguments.

Must be used below [@tg.guarentee_test](#guarantee_test), otherwise, it is ignored.

Brackets are not optional, meaning that it has to be used as 
`@tg.guarantee_usage()`, not just `@tg.guarantee_usage`.

A function decorated as follows:

```python 
@tg.guarantee_test()
@tg.guarantee_usage()
def foo():
    pass
```

with a unittest that looks something like this:

```python 
class TestExample(unittest.TestCase):
    @tg.implements_test_for(foo)
    def test_foo(self):
        self.assertTrue(True)
```

would lead to a [NotUsedInTestsError](#notusedintestserror) being raised. 

Guarantees that a given function or method is used by any test-function
that is decorated by [@tg.implements_test_for](#implements_test_for), if 
`@tg.implements_test_for` takes the function or method as an argument.


### `implements_test_for`

- `args`: Give any function or method that the corresponding test is meant for.
- `kwargs`: The value will be used like an `arg`, while the key will be ignored.

Functions and methods that weren't decorated by [@tg.guarantee_test](#guarantee_test) 
lead to a user-warning but are ignored otherwise.

Usage might look as follows:

```python 
class TestExample(unittest.TestCase):
    @implements_test_for(function1, function2, this_key_is_ignored=function3)
    def test_example(self):
        ...
```

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

`Exception`s are located under `tg.exceptions`.

There are two custom `Exception`s as presented below.

### `TestsNotImplementedError`

Members of `tg.exceptions.TestsNotImplementedError`:

- `functions` (type: `callable`): The callables that weren't mentioned in a 
[`@tg.implements_test_for`](#implements_test_for).
- `description` (type: `str`): The error string printed when the exception is raised
and not caught.

The output of raising this exception might look something like:

    pyguarantees.test_guarantees.exceptions.TestsNotImplementedError: 

        No tests were implemented for the following methods and functions: 
    
        1. Missing test-case for the following callable: 
            Name: 		foo
            Module: 	__main__
        2. Missing test-case for the following callable: 
            Name: 		bar
            Module: 	__main__

### `NotUsedInTestsError`

Members of `tg.exceptions.NotUsedInTestsError`:

- `functions` (type: `callable`): The callables that were mentioned in a 
[`@tg.implements_test_for`](#implements_test_for) but not used in the corresponding
test.
- `description` (type: `str`): The error string printed when the exception is raised
and not caught.

A possible error message might look like the following:
    

    The following methods and functions were not executed in their assigned tests: 

	1. The following callable was not called in its assigned tests: 
		Name: 		foo
		Module: 	__main__
		This callable is tested but not called in the following test-cases: 
					- Name: 	TestFoo.test_foo1
					   Module: 	__main__
					- Name: 	TestFoo.test_foo2
					   Module: 	__main__
	2. The following callable was not called in its assigned tests: 
		Name: 		bar
		Module: 	some_module
		This callable is tested but not called in the following test-cases: 
					- Name: 	TestBar.test_bar
					   Module: 	test_some_module
