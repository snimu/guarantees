import unittest

# Import unittest from their respective files
#   -> unittest.main() will run them all
from tests._test_types_numeric import TestNumericGuarantee
from tests._test_types_string import TestStringGuarantee
from tests._test_types_boolean import TestBooleanGuarantee
from tests._test_types_other import TestOther

# TODO(snimu) include tests for 'callback' in all TestCases


if __name__ == '__main__':
    unittest.main()
