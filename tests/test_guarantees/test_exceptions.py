import pytest
from pyguarantees import test_guarantees as tg


@pytest.mark.order(0)
def test_TestsNotImplementedError():
    @tg.guarantee_test()
    def fct(a):
        return a

    with pytest.raises(tg.exceptions.TestsNotImplementedError):
        tg.test_all_tests_implemented()

    @tg.implements_test_for(fct)
    def ensure_no_exception_at_end_of_pytest():
        fct(1)


@pytest.mark.order(1)
def test_NotUsedInTestsError():
    @tg.guarantee_test()
    @tg.guarantee_usage()
    def fct(a):
        return a

    @tg.implements_test_for(fct)
    def random_function():
        pass

    random_function()

    with pytest.raises(tg.exceptions.NotUsedInTestsError):
        tg.test_functions_used_in_tests()

    # test_functions_used_in_tests will be called at the end by pytest;
    #   make sure that it won't err
    _mark_as_used(fct)


def _mark_as_used(fct):
    tg._decorators.fdata[fct]["testcases_without_exec"] = None

