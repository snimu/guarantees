import pytest

from pyguarantees import functional_guarantees as fg


lst = [1, 2, 3]
tup = (1, 2, 3)
dic = {1: 1, 2: 2, 3: 3}
st = {1, 2, 3}
fst = frozenset(lst)
rng = range(1, 3, 1)


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


@fg.add_guarantees(param_guarantees=[
    fg.IsList("lst", minimum_len=1, maximum_len=3),
    fg.IsTuple("tup", minimum_len=1, maximum_len=3),
    fg.IsDict("dic", minimum_len=1, maximum_len=3),
    fg.IsSet("st", minimum_len=1, maximum_len=3),
    fg.IsFrozenSet("fst", minimum_len=1, maximum_len=3)
])
def minmax_fct(lst, tup, dic, st, fst):
    return lst, tup, dic, st, fst


@fg.add_guarantees(param_guarantees=[
    fg.IsList("lst", contains=[1, 2, 3]),
    fg.IsTuple("tup", contains=[1, 2, 3]),
    fg.IsSet("st", contains=[1, 2, 3]),
    fg.IsFrozenSet("fst", contains=[1, 2, 3])
])
def contains_fct(lst, tup, st, fst):
    return lst, tup, st, fst


@fg.add_guarantees(param_guarantees=[
    fg.IsDict("dic", has_keys=[1, 2, 3], has_values=[1, 2, 3])
])
def keysvals_fct(dic):
    return dic


class TestCollectionsGuarantee:
    def test_base_correct(self):
        base_fct(lst, tup, dic, st, fst, rng)

    def test_base_violations(self):
        def type_test(index: int):
            inputs = [lst, tup, dic, st, fst, rng]
            inputs[index] = 1   # Add false type at the index
            with pytest.raises(fg.exceptions.ParameterGuaranteesTypeError):
                base_fct(*inputs)

        for i in range(6):
            type_test(i)

    def test_minmax_len_correct(self):
        # Check correct inputs don't raise exceptions
        minmax_fct(lst, tup, dic, st, fst)

    def test_min_len_violations(self):
        too_shorts = [[], (), {}, set(), frozenset()]   # prepare false inputs

        def len_test_min(index):
            inputs = [lst, tup, dic, st, fst]
            inputs[index] = too_shorts[index]   # add false input at index
            with pytest.raises(fg.exceptions.ParameterGuaranteesValueError):
                minmax_fct(*inputs)

        for i in range(5):
            len_test_min(i)

    def test_max_len_violations(self):
        # Prepare false inputs
        base = [1, 2, 3, 4]
        too_longs = [base, tuple(base), {i: i for i in base}, set(base), frozenset(base)]

        def len_test_max(index):
            inputs = [lst, tup, dic, st, fst]
            inputs[index] = too_longs[index]
            with pytest.raises(fg.exceptions.ParameterGuaranteesValueError):
                minmax_fct(*inputs)

        for i in range(5):
            len_test_max(i)

    def test_contains_correct(self):
        contains_fct(lst, tup, st, fst)

    def test_contains_violated(self):
        # Prepare false inputs
        base = [1]
        false_inputs = [base, tuple(base), set(base), frozenset(base)]

        def contains_test(index):
            inputs = [lst, tup, st, fst]
            inputs[index] = false_inputs[index]
            with pytest.raises(fg.exceptions.ParameterGuaranteesValueError):
                contains_fct(*inputs)

        for i in range(4):
            contains_test(i)

    def test_has_keys_vals(self):
        keysvals_fct(dic)

        with pytest.raises(fg.exceptions.ParameterGuaranteesValueError):
            keysvals_fct({1: 1, 2: 2, "nope": 3})

        with pytest.raises(fg.exceptions.ParameterGuaranteesValueError):
            keysvals_fct({1: 1, 2: 2, 3: "nope"})
