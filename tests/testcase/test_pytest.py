import asyncio

import pyguarantees as pg
from tests.testcase import _fcts1, _fcts2


@pg.testcase.guaranteed()
@pg.testcase.calls()
def foo():
    return 1


@pg.testcase.guaranteed()
@pg.testcase.calls()
def generator_fct(lst: list):
    for item in lst:
        yield item


@pg.testcase.guaranteed()
@pg.testcase.calls()
async def async_fct(item):
    await asyncio.sleep(.1)
    return item


def not_guaranteed_fct():
    return "hello!"


class ExampleClass:
    cls_var = True

    def __init__(self):
        self.instance_var = True

    @staticmethod
    @pg.testcase.guaranteed()
    @pg.testcase.calls()
    def static_method():
        return True

    @classmethod
    @pg.testcase.guaranteed()
    @pg.testcase.calls()
    def class_method(cls):
        return cls.cls_var

    @pg.testcase.guaranteed()
    @pg.testcase.calls()
    def method(self):
        return self.instance_var

    def nested_method(self):
        @pg.testcase.guaranteed()
        @pg.testcase.calls()
        def function_in_method():
            return 1

        return function_in_method()


@pg.testcase.guaranteed()
@pg.testcase.calls()
class CallableClass:
    x = 1

    def __call__(self, *args, **kwargs):
        return args, kwargs


@pg.testcase.guaranteed()
@pg.testcase.calls()
class RegularClass:
    def __init__(self):
        self.x = 3


@pg.testcase.covers(foo, not_guaranteed_fct)
def test_same_module():
    assert foo() == 1


@pg.testcase.covers(foo)
def test_same_module_again():
    assert foo() == 1


@pg.testcase.covers(_fcts1.some_fct, _fcts1.SomeClass.some_method)
def test_fcts1():
    assert _fcts1.some_fct(1, 2, 3) == (1, 2, 3)
    assert _fcts1.SomeClass().some_method() ==  1


@pg.testcase.covers(_fcts2.another_fct)
def test_fcts2():
    pass


@pg.testcase.covers(generator_fct)
def test_generator_fct():
    for val in generator_fct([1, 1, 1]):
        assert val == 1


@pg.testcase.covers(async_fct)
def test_async_fct():
    for i in range(3):
        assert asyncio.run(async_fct(i)) == i


@pg.testcase.covers(
    ExampleClass.static_method,
    ExampleClass.class_method,
    ExampleClass.method
)
def test_example_class():
    assert ExampleClass.static_method()
    assert ExampleClass.class_method()
    assert ExampleClass().method()


@pg.testcase.covers(CallableClass)
def test_callble_class():
    CallableClass()(CallableClass.x)


@pg.testcase.covers(RegularClass)
def test_regular_class():
    RegularClass()
