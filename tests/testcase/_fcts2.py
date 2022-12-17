import pyguarantees as pg


@pg.testcase.guaranteed()
def another_fct():
    return 0
