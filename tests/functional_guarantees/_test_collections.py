import unittest

from pyguarantees import functional_guarantees as fg


class TestCollectionsGuarantee(unittest.TestCase):
    def setUp(self) -> None:
        self.lst = [1, 2, 3]
        self.tup = (1, 2, 3)
        self.dic = {1: 1, 2: 2, 3: 3}
        self.st = {1, 2, 3}
        self.fst = frozenset(self.lst)
        self.rng = range(1, 3, 1)

        @fg.add_guarantees(param_guarantees=[
            fg.IsList("lst"),
            fg.IsTuple("tup"),
            fg.IsDict("dic"),
            fg.IsSet("st"),
            fg.IsFrozenSet("fst"),
            fg.IsRange("rng")
        ])
        def base_fct(lst, tup, dic, st, fst, rng):
            return lst, tup, dic, st, fst, rng

        self.base_fct = base_fct

        @fg.add_guarantees(param_guarantees=[
            fg.IsList("lst", minimum_len=1, maximum_len=3),
            fg.IsTuple("tup", minimum_len=1, maximum_len=3),
            fg.IsDict("dic", minimum_len=1, maximum_len=3),
            fg.IsSet("st", minimum_len=1, maximum_len=3),
            fg.IsFrozenSet("fst", minimum_len=1, maximum_len=3)
        ])
        def minmax_fct(lst, tup, dic, st, fst):
            return lst, tup, dic, st, fst

        self.minmax_fct = minmax_fct

        @fg.add_guarantees(param_guarantees=[
            fg.IsList("lst", contains=[1, 2, 3]),
            fg.IsTuple("tup", contains=[1, 2, 3]),
            fg.IsSet("st", contains=[1, 2, 3]),
            fg.IsFrozenSet("fst", contains=[1, 2, 3])
        ])
        def contains_fct(lst, tup, st, fst):
            return lst, tup, st, fst

        self.contains_fct = contains_fct

        @fg.add_guarantees(param_guarantees=[
            fg.IsDict("dic", has_keys=[1, 2, 3], has_values=[1, 2, 3])
        ])
        def keysvals_fct(dic):
            return dic

        self.keysvals_fct = keysvals_fct

    def test_base_correct(self):
        # Check working inputs produce no errors
        self.base_fct(self.lst, self.tup, self.dic, self.st, self.fst, self.rng)

    def test_base_violations(self):
        def type_test(index: int):
            inputs = [self.lst, self.tup, self.dic, self.st, self.fst, self.rng]
            inputs[index] = 1   # Add false type at the index
            self.assertRaises(
                fg.exceptions.ParameterGuaranteesTypeError,
                self.base_fct, *inputs
            )

        for i in range(6):
            type_test(i)

    def test_minmax_len_correct(self):
        # Check correct inputs don't raise exceptions
        self.minmax_fct(self.lst, self.tup, self.dic, self.st, self.fst)

    def test_min_len_violations(self):
        too_shorts = [[], (), {}, set(), frozenset()]   # prepare false inputs

        def len_test_min(index):
            inputs = [self.lst, self.tup, self.dic, self.st, self.fst]
            inputs[index] = too_shorts[index]   # add false input at index
            self.assertRaises(
                fg.exceptions.ParameterGuaranteesValueError,
                self.minmax_fct, *inputs
            )

        for i in range(5):
            len_test_min(i)

    def test_max_len_violations(self):
        # Prepare false inputs
        base = [1, 2, 3, 4]
        too_longs = [base, tuple(base), {i: i for i in base}, set(base), frozenset(base)]

        def len_test_max(index):
            inputs = [self.lst, self.tup, self.dic, self.st, self.fst]
            inputs[index] = too_longs[index]
            self.assertRaises(
                fg.exceptions.ParameterGuaranteesValueError,
                self.minmax_fct, *inputs
            )

        for i in range(5):
            len_test_max(i)

    def test_contains_correct(self):
        self.contains_fct(self.lst, self.tup, self.st, self.fst)

    def test_contains_violated(self):
        # Prepare false inputs
        base = [1]
        false_inputs = [base, tuple(base), set(base), frozenset(base)]

        def contains_test(index):
            inputs = [self.lst, self.tup, self.st, self.fst]
            inputs[index] = false_inputs[index]
            self.assertRaises(
                fg.exceptions.ParameterGuaranteesValueError,
                self.contains_fct, *inputs
            )

        for i in range(4):
            contains_test(i)

    def test_has_keys_vals(self):
        self.keysvals_fct(self.dic)

        self.assertRaises(
            fg.exceptions.ParameterGuaranteesValueError,
            self.keysvals_fct,
            {1: 1, 2: 2, "nope": 3}
        )

        self.assertRaises(
            fg.exceptions.ParameterGuaranteesValueError,
            self.keysvals_fct,
            {1: 1, 2: 2, 3: "nope"}
        )
