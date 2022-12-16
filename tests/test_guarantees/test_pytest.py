from pyguarantees.test_guarantees import test_all_tests_implemented, test_functions_used_in_tests
from pyguarantees import test_guarantees as tg


@tg.guarantee_test()
@tg.guarantee_usage()
def foo():
    return 1


@tg.implements_test_for(foo)
def test_foo():
    foo()
