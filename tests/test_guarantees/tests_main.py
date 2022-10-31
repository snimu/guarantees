import unittest

from guarantees import test_guarantees as tg

# Test:
#   file defines 2 fcts with guarantees
#   testfile imports fct1 from file but not fct2
#   -> should only check for fct1
# Test:
#   guarantee_usage


@tg.guarantee_usage
def foo():
    return 1


tg.guarantee_test_for(foo)


class TestRegisters(unittest.TestCase):
    @tg.implements_test_for(foo)
    def test_implements(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()