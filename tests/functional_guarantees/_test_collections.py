import unittest

import pyguarantees.functional_guarantees.exceptions
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

    def test_base(self):
        # Check working inputs produce no errors
        self.base_fct(self.lst, self.tup, self.dic, self.st, self.fst, self.rng)

        # Check false inputs
        try:
            self.base_fct(1, self.tup, self.dic, self.st, self.fst, self.rng)
            self.assertTrue(False)   # param lst should have raised exception
        except fg.exceptions.ParameterGuaranteesTypeError:
            self.assertTrue(True)    # successfully raised exception

        try:
            self.base_fct(self.lst, 1, self.dic, self.st, self.fst, self.rng)
            self.assertTrue(False)   # param tup should have raised exception
        except fg.exceptions.ParameterGuaranteesTypeError:
            self.assertTrue(True)    # successfully raised exception

        try:
            self.base_fct(self.lst, self.tup, 1, self.st, self.fst, self.rng)
            self.assertTrue(False)   # param dic should have raised exception
        except fg.exceptions.ParameterGuaranteesTypeError:
            self.assertTrue(True)    # successfully raised exception

        try:
            self.base_fct(self.lst, self.tup, self.dic, 1, self.fst, self.rng)
            self.assertTrue(False)   # param st should have raised exception
        except fg.exceptions.ParameterGuaranteesTypeError:
            self.assertTrue(True)    # successfully raised exception

        try:
            self.base_fct(self.lst, self.tup, self.dic, self.st, 1, self.rng)
            self.assertTrue(False)   # param fst should have raised exception
        except fg.exceptions.ParameterGuaranteesTypeError:
            self.assertTrue(True)    # successfully raised exception

        try:
            self.base_fct(self.lst, self.tup, self.dic, self.st, self.fst, 1)
            self.assertTrue(False)   # param rng should have raised exception
        except fg.exceptions.ParameterGuaranteesTypeError:
            self.assertTrue(True)    # successfully raised exception

    def test_minmax_len_correct(self):
        # Check correct inputs don't raise exceptions
        self.minmax_fct(self.lst, self.tup, self.dic, self.st, self.fst)

    def test_minmax_len_violation_lst(self):
        try:
            self.minmax_fct([], self.tup, self.dic, self.st, self.fst)
            self.assertTrue(False)   # param lst should have raised an exception
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)    # successfully raised exception

        try:
            self.minmax_fct([1, 2, 3, 4], self.tup, self.dic, self.st, self.fst)
            self.assertTrue(False)   # param lst should have raised an exception
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)    # successfully raised exception

    def test_minmax_len_violation_tup(self):
        try:
            self.minmax_fct(self.lst, (), self.dic, self.st, self.fst)
            self.assertTrue(False)   # param lst should have raised an exception
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)    # successfully raised exception

        try:
            self.minmax_fct(self.lst, (1, 2, 3, 4), self.dic, self.st, self.fst)
            self.assertTrue(False)   # param lst should have raised an exception
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)    # successfully raised exception

    def test_minmax_len_violation_dic(self):
        try:
            self.minmax_fct(self.lst, self.tup, {}, self.st, self.fst)
            self.assertTrue(False)   # param lst should have raised an exception
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)    # successfully raised exception

        try:
            wrong_dict = {1: 1, 2: 2, 3: 3, 4: 4}
            self.minmax_fct(self.lst, self.tup, wrong_dict, self.st, self.fst)
            self.assertTrue(False)   # param lst should have raised an exception
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)    # successfully raised exception

    def test_minmax_len_violation_set(self):
        try:
            self.minmax_fct(self.lst, self.tup, self.dic, set(), self.fst)
            self.assertTrue(False)   # param lst should have raised an exception
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)    # successfully raised exception

        try:
            wrong_set = {1, 2, 3, 4}
            self.minmax_fct(self.lst, self.tup, self.dic, wrong_set, self.fst)
            self.assertTrue(False)   # param lst should have raised an exception
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)    # successfully raised exception

    def test_minmax_len_violation_fset(self):
        try:
            self.minmax_fct(self.lst, self.tup, self.dic, self.st, frozenset())
            self.assertTrue(False)   # param lst should have raised an exception
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)    # successfully raised exception

        try:
            wrong_fset = frozenset({1, 2, 3, 4})
            self.minmax_fct(self.lst, self.tup, self.dic, self.st, wrong_fset)
            self.assertTrue(False)   # param lst should have raised an exception
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)    # successfully raised exception

    def test_contains_correct(self):
        self.contains_fct(self.lst, self.tup, self.st, self.fst)

    def test_contains_violated_lst(self):
        try:
            self.contains_fct([1, 2], self.tup, self.st, self.fst)
            self.assertTrue(False)   # param lst should have raised an exception
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)    # successfully raised exception

    def test_contains_violated_tup(self):
        try:
            self.contains_fct(self.lst, (1, 2), self.st, self.fst)
            self.assertTrue(False)   # param lst should have raised an exception
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)    # successfully raised exception

    def test_contains_violated_st(self):
        try:
            self.contains_fct(self.lst, self.tup, {1, 2}, self.fst)
            self.assertTrue(False)   # param lst should have raised an exception
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)    # successfully raised exception

    def test_contains_violated_fst(self):
        try:
            self.contains_fct(self.lst, self.tup, self.st, frozenset((1, 2)))
            self.assertTrue(False)   # param lst should have raised an exception
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)    # successfully raised exception

    def test_has_keys_vals(self):
        self.keysvals_fct(self.dic)

        try:
            self.keysvals_fct({1: 1, 2: 2, "nope": 3})
            self.assertTrue(False)    # param dic should have raised exception
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)

        try:
            self.keysvals_fct({1: 1, 2: 2, 3: "nope"})
            self.assertTrue(False)    # param dic should have raised exception
        except fg.exceptions.ParameterGuaranteesValueError:
            self.assertTrue(True)

# TODO: Refactor: one class for each of the four functions
