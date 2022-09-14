import unittest
from ._data import TestGuarantees


class TestCase(unittest.TestCase):
    @classmethod
    def tearDownClass(cls) -> None:
        TestGuarantees.finish()   # raises exceptions
