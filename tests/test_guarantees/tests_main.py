import unittest

from guarantees import test_guarantees as tg
from tests.test_guarantees import _fcts1, _fcts2


@tg.guarantee_test()
@tg.guarantee_usage()
def foo():
    return 1


class TestRegisters(unittest.TestCase):
    @tg.implements_test_for(foo)
    def test_same_module(self):
        self.assertEqual(foo(), 1)

    @tg.implements_test_for(foo)
    def test_same_module_again(self):
        self.assertEqual(foo(), 1)

    @tg.implements_test_for([_fcts1.some_fct, _fcts1.SomeClass.some_method])
    def test_fcts1(self):
        self.assertEqual(_fcts1.some_fct(1, 2, 3), (1, 2, 3))
        self.assertEqual(_fcts1.SomeClass().some_method(), 1)

    @tg.implements_test_for(_fcts2.another_fct)
    def test_fcts2(self):
        self.assertTrue(True)


if __name__ == "__main__":
    tg.main()
