import guarantees.test_guarantees as tg


@tg.guarantee_test()
def some_fct(a, b, c):
    return a, b, c


class SomeClass:
    @tg.guarantee_test()
    def some_method(self):
        return 1
