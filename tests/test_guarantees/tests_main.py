import unittest

from guarantees import test_guarantees as tg


@tg.guarantee_test()
def foo():
    return 1


class TestRegisters(unittest.TestCase):
    @tg.implements_test_for(foo)
    def test_implements(self):
        self.assertEquals(foo(), 1)


if __name__ == "__main__":
    tg.main()
