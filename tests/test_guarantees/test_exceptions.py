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
    pass   # TODO
