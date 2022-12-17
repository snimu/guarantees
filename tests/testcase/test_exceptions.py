import pytest
import pyguarantees as pg


@pytest.mark.order(0)
def test_TestsNotImplementedError():
    @pg.testcase.guaranteed()
    def fct(a):
        return a

    with pytest.raises(pg.exceptions.testcase.TestsNotImplementedError):
        pg.pytests.test_all_tests_implemented()

    @pg.testcase.covers(fct)
    def ensure_no_exception_at_end_of_pytest():
        fct(1)


@pytest.mark.order(1)
def test_NotUsedInTestsError():
    @pg.testcase.guaranteed()
    @pg.testcase.calls()
    def fct(a):
        return a

    @pg.testcase.covers(fct)
    def random_function():
        pass

    random_function()

    with pytest.raises(pg.exceptions.testcase.NotUsedInTestsError):
        pg.pytests.test_functions_used_in_tests()

    # test_functions_used_in_tests will be called at the end by pytest;
    #   make sure that it won't err
    _mark_as_used(fct)


def _mark_as_used(fct):
    pg.testcase.fdata[fct]["testcases_without_exec"] = None

