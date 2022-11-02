class Wrapper:
    def __init__(self, fct: callable, guarantee_usage: bool):
        self.fct = fct
        self.guarantee_usage = guarantee_usage
        self.has_test = False
        self.counter = 0
        self.was_called = True

    def __call__(self, *args, **kwargs):
        self.counter += 1
        return self.fct(*args, **kwargs)
