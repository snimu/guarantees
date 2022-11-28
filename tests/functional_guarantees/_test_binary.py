import unittest
from pyguarantees import functional_guarantees as fg


class TestBinary(unittest.TestCase):
    def setUp(self) -> None:
        @fg.add_guarantees(param_guarantees=[
            fg.IsBytes("a"),
            fg.IsByteArray("b"),
            fg.IsMemoryView("c")
        ])
        def fct(a, b, c):
            return a, b, c

        @fg.add_guarantees(param_guarantees=[
            fg.IsBytes("a", force_conversion=True),
            fg.IsByteArray("b", force_conversion=True),
            fg.IsMemoryView("c", force_conversion=True)
        ])
        def fct_conversion(a, b, c):
            return a, b, c

        self.fct = fct
        self.fct_conversion = fct_conversion

        self.bytes = b"123"
        self.bytearray = bytearray(self.bytes)
        self.memoryview = memoryview(self.bytes)

    def test_binary_correct(self):
        self.fct(self.bytes, self.bytearray, self.memoryview)
        by, byarr, mem = self.fct_conversion(123, 123, b"123")
        self.assertIsInstance(by, bytes)
        self.assertIsInstance(byarr, bytearray)
        self.assertIsInstance(mem, memoryview)

    def test_false_input_bytes(self):
        try:
            self.fct(123, self.bytearray, self.memoryview)
            self.assertTrue(False)   # should have raised an exception
        except fg.exceptions.ParameterGuaranteesTypeError:
            self.assertTrue(True)    # successfully raised exception

    def test_false_input_bytearray(self):
        try:
            self.fct(self.bytes, 123, self.memoryview)
            self.assertTrue(False)   # should have raised an exception
        except fg.exceptions.ParameterGuaranteesTypeError:
            self.assertTrue(True)    # successfully raised exception

    def test_false_input_memoryview(self):
        try:
            self.fct(self.bytes, self.bytearray, 123)
            self.assertTrue(False)   # should have raised an exception
        except fg.exceptions.ParameterGuaranteesTypeError:
            self.assertTrue(True)    # successfully raised exception
