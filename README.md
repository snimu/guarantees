# pyguarantees

*Guarantee testcases for callables, constrain parameters and return values of callables.*

**Project**

![PyPI Version](https://img.shields.io/pypi/v/pyguarantees)
![Wheel](https://img.shields.io/pypi/wheel/pyguarantees)

**Info**


![License](https://img.shields.io/github/license/snimu/guarantees)
![Python Versions](https://img.shields.io/pypi/pyversions/pyguarantees)

**Tests**

![Tests](https://github.com/snimu/guarantees/actions/workflows/tests.yml/badge.svg)
![Coverage](coverage.svg)

**Installation&mdash;Pip**

```bash
pip3 install pyguarantees
```


# tests

"I will have to write a unittest for this function later", you say. This package ensures that you 
won't forget.

"Why does this function fail? I've tested it... omg I didn't even call it in my TestCase." Use this 
package to make sure that a function/method will be called or a class instance constructed 
in its respective `TestCase`.

Can be used for `unittest` and `pytest`.

## Example unittest

```python 
import unittest
import pyguarantees as pg
from some_package import some_fct_with_test_guarantee


@pg.testcase.guaranteed()
@pg.testcase.calls()  # make sure that this is called in all its tests
def add_one(a):
    return a + 1


@pg.testcase.guaranteed()
@pg.testcase.calls()  # Makes sure that __init__ is called in the test
class RegularClass:
    def __init__(self):
        self.x = 2


class ExampleTest(unittest.TestCase):
    @pg.testcase.covers(add_one, some_fct_with_test_guarantee)
    def test_some_stuff(self):
        val = add_one(1)
        self.assertEqual(val, 2)
        # some_fct_with_test_guarantees has no @pg.testcase.call
        #   -> doesn't have to be called here.
      

    @pg.testcase.covers(RegularClass)
    def test_regular_class(self):
        regular_class = RegularClass()
        ...


if __name__ == '__main__':
    pg.unittests.main()
```

As in the example, `pyguarantees` will be abbreviated with `pg` from here on out.

Failing to use an [@pg.testcase.covers](#covers) for a function or method decorated with [@pg.testcase.guaranteed](#guaranteed)
leads to a [tg.exceptions.testcase.TestsNotImplementedError](#testsnotimplementederror), while failing to use this function or method in the 
corresponding test will lead to a [tg.exceptions.testcase.NotUsedInTestsError](#notusedintestserror) if it is decorated by 
[@tg.guarantee_usage](#guarantee_usage). These exceptions are only raised if the `unittest.TestCase` are called first 
and then checked by [pg.unittests.enforce](#enforce), or [pg.unittests.main](#main) is called to do both automatically.

Currently doesn't work with nested functions (defined inside of other callables). This might be fixed at some point.


## Example pytest

```python
# These imports are unused but necessary for pytest to find the tests that 
#  enforce the guarantees from tg
from pyguarantees.pytests import
    test_all_tests_implemented, test_functions_used_in_tests
import pyguarantees as pg


class ExampleClass:
    @pg.testcase.guaranteed()  # tg.main will raise exception if there is not test for this method
    def method(self):
        return self

    @classmethod  # works for classmethods
    @pg.testcase.guaranteed()  # @pg.testcase.calls possible in any of these methods, but optional
    def class_method(cls):
        return cls

    @staticmethod  # works for staticmethods
    @pg.testcase.guaranteed()
    @pg.testcase.calls()
    def static_method():
        return "static!"


@pg.testcase.covers(
    ExampleClass.method,
    ExampleClass.class_method,
    ExampleClass.static_method
)
def test_example_class():
    assert ExampleClass.static_method() == "static!"
```

This is even simpler: just use [@pg.testcase.guaranteed](#guaranteed), [@pg.testcase.calls](#calls),
and [@pg.testcase.covers](#covers) as in [Example unittest](#example-unittest). No 
need to call [pg.unittests.main](#main) or [tg.enforce](#enforce); instead, import (but don't use) 
[pg.pytests.test_all_tests_implemented](#testalltestsimplemented) and 
[pg.pytests.test_functions_used_in_tests](#testfunctionsusedintests) and then run `pytest`.

**IMPORTANT**: If you use `pytest.mark.order` from the [pytest-order](https://pypi.org/project/pytest-order/)-package,
don't use `pytest.mark.order(-1)` or `pytest.mark.order(-2)` on your tests&mdash;it is important that 
[test_all_tests_implemented](#testalltestsimplemented) and [test_functions_used_in_tests](#testfunctionsusedintests) 
are used last by `pytest`.


## Decorators

The three decorators shown below have no effect without the [functions](#functions) 
of this package, specifically running [main](#main) or [enforce](#enforce) for `unittest`, 
and simply importing [test_all_tests_implemented](#testalltestsimplemented) and 
[test_functions_used_in_tests](#testfunctionsusedintests) into one of your test-files.


### guaranteed

Takes no arguments.

Any function, method, or class (except, for the moment, ones nested inside of other callables) 
decorated with `@pg.testcase.guaranteed`
that is in the scope of unittest will force unittest to throw an exception should 
it not be in an [@pg.testcase.covers](#covers).

Currently, it is necessary to include the brackets&mdash;`()`&mdash; so that 
the function is registered. This executes the decorator once but not the callable that 
it decorates, making it computationally inexpensive.

Having a function (or method) decorated like follows:

```python
@pg.testcase.guaranteed()
def foo():
  pass
```

but not having a test in your `unittest.TestCase` decorated by `@pg.testcase.covers(foo)` 
would lead to a [TestsNotImplementedError](#testsnotimplementederror) being raised.

The same works for classes.


### calls

Takes no arguments.

Must be used below [@pg.testcase.guaranteed](#guaranteed), otherwise it is ignored.

Just like with `@pg.testcase.guaranteed`, brackets are not optional, but the execution of 
the decorator is computationally inexpensive.

A function decorated as follows:

```python 
@pg.testcase.guaranteed()
@pg.testcase.calls()
def foo():
  pass
```

with a unittest that looks something like this:

```python 
# for unittest:
class TestExample(unittest.TestCase):
  @pg.testcase.covers(foo)
  def test_foo(self):
    ...  # some code that doesn't call foo


# for pytest:
@pg.testcase.covers(foo)
def test_foo():
  ...  # some code that doesn't call foo
```

would lead to a [NotUsedInTestsError](#notusedintestserror) being raised. 

In this scenario, if `foo` is an argument in several 
[@pg.testcase.covers](#covers),
`@pg.testcase.calls` makes certain that `foo` is used in every test-function 
decorated in such a way.

Special case: For classes, `@pg.testcase.calls` guarantees that `__init__` is called.
For a callable class, this still holds; to guarantee that the `__call__`-method is called
in the test, it has to be decorated by `@pg.testcase.calls` itself, not the class it belongs to. 


### covers

- `args`: Give any function or method that the corresponding test is meant for.
- `kwargs`: The value will be used like an `arg`, while the key will be ignored.

Functions and methods that weren't decorated by [@pg.testcase.guaranteed](#guaranteed) 
lead to a user-warning but are ignored otherwise.

Usage might look as follows:

```python 
# for unittest:
class TestExample(unittest.TestCase):
  @pg.testcase.covers(function1, function2, this_key_is_ignored=function3)
  def test_example(self):
    ...


# for pytest:
@pg.testcase.covers(function1, function2, this_key_is_ignored=function3)
def test_example():
  ...
```

## Functions

For `unittest`, at least one of [main](#main) or [enforce](#enforce) 
has to be used for the [decorators](#decorators)
to have an effect. 

For `pytest`, both [test_all_tests_implemented](#testalltestsimplemented) 
and [test_functions_used_in_tests](#testfunctionsusedintests) have to be imported 
into one of your test-files.

### enforce

Takes no arguments. This will likely change in the future to make it more adaptable.

Run this after running all your unittests. This runs additional unittests that 
check which functions violated their guarantees and raise [exceptions](#exceptionstestcase) 
accordingly.

It is recommended to only use this function when using a complicated unittest-setup.
When using `unittest.main()`, it is recommended to use `pg.testcase.main()` instead.

### main

Takes no arguments. This will likely change in the future to make it more adaptable.

Calls `unittest.main()` followed by [pg.unittests.enforce](#enforce).

### test_all_tests_implemented

Takes no arguments.

Import this into one of your files for [@pg.testcase.guaranteed](#guaranteed) and 
[@pg.testcase.covers](#covers) to have any effect.

### test_functions_used_in_tests

Takes no arguments.

Import this and [test_all_tests_implemented](#testalltestsimplemented) 
into one of your files for [@pg.testcase.guaranteed](#guaranteed) to 
have any effect.

## exceptions.testcase

`Exceptions` are located under `pg.exceptions.testcase`.

There are two custom `Exceptions` as presented below.

### TestsNotImplementedError

Arguments of `tg.exceptions.testcase.TestsNotImplementedError`:

- `functions` (type `callable`): The callables that weren't mentioned in a 
[@pg.testcase.covers](#covers).

Members of `tg.exceptions.testcase.TestsNotImplementedError`:

- `functions` (type `callable`): The callables that weren't mentioned in a 
[@pg.testcase.covers](#covers).
- `description` (type `str`): The error string printed when the exception is raised
and not caught.

The output of raising this exception might look something like:

    <Traceback...>

    pyguarantees.exceptions.testcase.TestsNotImplementedError: 

        No tests were implemented for the following methods and functions: 
    
        1. Missing test-case for the following callable: 
            Name: 		foo
            Module: 	__main__
        2. Missing test-case for the following callable: 
            Name: 		bar
            Module: 	__main__

### NotUsedInTestsError
Arguments of `tg.exceptions.testcase.NotUsedInTestsError`:

- `functions` (type: `callable`): The callables that were mentioned in a 
[@pg.testcase.covers](#covers) but not used in the corresponding
test.

Members of `tg.exceptions.NotUsedInTestsError`:

- `functions` (type: `callable`): The callables that were mentioned in a 
[@pg.testcase.covers](#covers) but not used in the corresponding
test.
- `description` (type: `str`): The error string printed when the exception is raised
and not caught.

A possible error message might look like the following:
    
    <Traceback...>

    pyguarantees.exceptions.testcase.NotUsedInTestsError:

    The following objects were not used in their assigned tests: 

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


# constraints

Few things are more useful in programming than the ability to constrain a program's possible behaviors 
and communicate those constraints clearly in code. Statically typed languages do this with types, scope modifiers, 
and lifetime modifiers, among others (`int`, `static`, `private`, `const`, etc.). These are static constraints 
in that they are evaluated statically, before runtime.

Oftentimes, a program also has dynamic constraints, evaluated during runtime&mdash;assertions, for example. 
A function dealing with division, for example, has to deal with the special case of division by zero. 

`pyguarantees`, abbreviated by `pg` again, enables both types of guarantees to be 
defined in Python where they should happen: function (or method) signatures. This is where statically typed 
languages put their static constraints (a typical function signature looks something like 
`scope-etc-modifiers return-type function-name(parameter-type parameter-name)`) and where in my opinion, dynamic 
constraints belong as well.

This might have the following advantages:
- Make code more readable by having constraints in a predefined place.
- Make code easier to write by providing important information about APIs in a glancable way.
- Make it possible to include information on dynamic constraints in automatically generated documentation.
- Encourage programmers to think about these constraints while writing the functions&mdash;a type of 
test-driven development directly at the function (seeing parts of the "tests" in the function-signature
might assist readability of code, as well). 

This package is an attempt to open up at least some of these advantages to Python-users at least partially, 
given the constraints of the Python-language. 

## Example

```python
import numpy as np
import pyguarantees as pg
from pyguarantees.constraints import IsInt, IsClass, DynamicCheck

from your_module import your_custom_error_callback


# One of many built-in guarantees using one of many built-in options
@pg.constrain.parameters(num=IsInt(minimum=3))
def add_one(num):
  return num + 1


# Use IsClass to guarantee all types and classes that don't have specific constraints 
#  in pg.constraints. If they do, it is recommended to use those specific constraints.
@pg.constrain.parameters(
  X=IsClass(
    class_type=np.ndarray,
    dynamic_checks=[
      DynamicCheck(check=lambda x: x.min() > 0, description="min: 0"),
      DynamicCheck(check=lambda x: x.var() < 5, description="var < 5"),
      DynamicCheck(check=lambda x: x.shape == (3, 80, 80), description="shape (3, 80, 80")
    ],
    error_callback=your_custom_error_callback
  ),
  mean=IsClass(class_type=np.ndarray),
  std=IsClass(class_type=np.ndarray)
)
@pg.constrain.returns(IsClass(class_type=np.ndarray))
def normalize(X, mean, std):
  return (X - mean) / std
```



> this README is currently under development. More is coming.