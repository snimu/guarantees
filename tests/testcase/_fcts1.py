import pyguarantees as pg


@pg.testcase.guaranteed()
@pg.testcase.calls()
def some_fct(a, b, c):
    return a, b, c


class SomeClass:
    @pg.testcase.guaranteed()
    def some_method(self):
        return 1
