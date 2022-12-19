import pytest
import pyguarantees as pg


def test_handle_error_none():
    with pytest.raises(AssertionError):
        pg._constraints._util.error_handeling.handle_error(
            where="internal",
            type_or_value="type",
            guarantee=None,   # here is the cause of the error
            parameter_name="",
            what_dict={}
        )
