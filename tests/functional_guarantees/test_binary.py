import pytest

from pyguarantees import functional_guarantees as fg


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


class TestBinary:
    def test_binary_correct(self):
        fct(b"123", bytearray(b"123"), memoryview(b"123"))
        by, byarr, mem = fct_conversion(123, 123, b"123")
        assert isinstance(by, bytes)
        assert isinstance(byarr, bytearray)
        assert isinstance(mem, memoryview)

    def test_false_input_bytes(self):
        with pytest.raises(fg.exceptions.ParameterGuaranteesTypeError):
            fct(123, bytearray(b"123"), memoryview(b"123"))

    def test_false_input_bytearray(self):
        with pytest.raises(fg.exceptions.ParameterGuaranteesTypeError):
            fct(b"123", 123, memoryview(b"123"))

    def test_false_input_memoryview(self):
        with pytest.raises(fg.exceptions.ParameterGuaranteesTypeError):
            fct(b"123", bytearray(b"123"), 123)
