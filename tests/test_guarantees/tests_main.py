import unittest
import asyncio

from pyguarantees import test_guarantees as tg
from tests.test_guarantees import _fcts1, _fcts2


@tg.guarantee_test()
@tg.guarantee_usage()
def foo():
    return 1


@tg.guarantee_test()
@tg.guarantee_usage()
def generator_fct(lst: list):
    for item in lst:
        yield item


@tg.guarantee_test()
@tg.guarantee_usage()
async def async_fct(item):
    await asyncio.sleep(.1)
    return item


class ExampleClass:
    cls_var = True

    def __init__(self):
        self.instance_var = True

    @staticmethod
    @tg.guarantee_test()
    @tg.guarantee_usage()
    def static_method():
        return True

    @classmethod
    @tg.guarantee_test()
    @tg.guarantee_usage()
    def class_method(cls):
        return cls.cls_var

    @tg.guarantee_test()
    @tg.guarantee_usage()
    def method(self):
        return self.instance_var

    def nested_method(self):
        @tg.guarantee_test()
        @tg.guarantee_usage()
        def function_in_method():
            return 1

        return function_in_method()


@tg.guarantee_test()
@tg.guarantee_usage()
class CallableClass:
    x = 1

    def __call__(self, *args, **kwargs):
        return args, kwargs


@tg.guarantee_test()
@tg.guarantee_usage()
class RegularClass:
    def __init__(self):
        self.x = 3


class TestRegisters(unittest.TestCase):
    @tg.implements_test_for(foo)
    def test_same_module(self):
        self.assertEqual(foo(), 1)

    @tg.implements_test_for(foo)
    def test_same_module_again(self):
        self.assertEqual(foo(), 1)

    @tg.implements_test_for(_fcts1.some_fct, _fcts1.SomeClass.some_method)
    def test_fcts1(self):
        self.assertEqual(_fcts1.some_fct(1, 2, 3), (1, 2, 3))
        self.assertEqual(_fcts1.SomeClass().some_method(), 1)

    @tg.implements_test_for(_fcts2.another_fct)
    def test_fcts2(self):
        self.assertTrue(True)

    @tg.implements_test_for(generator_fct)
    def test_generator_fct(self):
        for val in generator_fct([1, 1, 1]):
            self.assertEqual(val, 1)

    @tg.implements_test_for(async_fct)
    def test_async_fct(self):
        for i in range(3):
            self.assertEqual(asyncio.run(async_fct(i)), i)

    @tg.implements_test_for(
        ExampleClass.static_method,
        ExampleClass.class_method,
        ExampleClass.method
    )
    def test_example_class(self):
        self.assertTrue(ExampleClass.static_method())
        self.assertTrue(ExampleClass.class_method())
        self.assertTrue(ExampleClass().method())

    @tg.implements_test_for(CallableClass)
    def test_callble_class(self):
        CallableClass()(CallableClass.x)

    @tg.implements_test_for(RegularClass)
    def test_regular_class(self):
        RegularClass()


if __name__ == "__main__":
    tg.main()
