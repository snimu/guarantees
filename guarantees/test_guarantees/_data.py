class TestGuarantees:
    functions = {}

    @classmethod
    def register_for_testing(cls, name, namespace=None, fct=None):
        full_name = cls.full_name(name, namespace)

        cls.functions[full_name] = {
            "has_test": False,
            "signature": fct,
            "counter": 0,
            "was_called": True
        }

    @classmethod
    def increment_counter(cls, name, namespace=None):
        full_name = cls.full_name(name, namespace)
        if full_name not in cls.functions.keys():
            return

        cls.functions[full_name]["counter"] += 1

    @classmethod
    def reset_counter(cls, name, namespace=None):
        full_name = cls.full_name(name, namespace)
        if full_name not in cls.functions.keys():
            return

        cls.functions[full_name]["counter"] = 0

    @classmethod
    def signal_has_test(cls, name, namespace):
        full_name = cls.full_name(name, namespace)
        if full_name not in cls.functions.keys():
            return

        cls.functions[full_name]["has_test"] = True

    @classmethod
    def use_guaranteed(cls, name, namespace):
        full_name = cls.full_name(name, namespace)
        if full_name not in cls.functions.keys():
            return

        if type(cls.functions[full_name]["signature"]) is callable:
            return True
        return False

    @classmethod
    def set_was_called_false(cls, name, namespace):
        full_name = cls.full_name(name, namespace)
        if full_name not in cls.functions.keys():
            return

        cls.functions[full_name]["was_called"] = False

    @classmethod
    def contains(cls, name, namespace=None):
        full_name = cls.full_name(name, namespace)

        if full_name in cls.functions.keys():
            return True
        return False

    @classmethod
    def get_counter(cls, name, namespace=None):
        return cls.functions[cls.full_name(name, namespace)]["counter"]

    @classmethod
    def full_name(cls, name, namespace=None):
        full_name = name
        if namespace is not None and type(namespace) is str:
            full_name = namespace + "/" + name

        return full_name

    @classmethod
    def finish(cls):
        pass
