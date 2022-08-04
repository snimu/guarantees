import unittest

# Import unittest from their respective files
#   -> unittest.main() will run them all
from tests._test_types_numeric import TestNumericGuarantee
from tests._test_types_string import TestStringGuarantee
from tests._test_types_boolean import TestBooleanGuarantee
from tests._test_types_other import TestOther
from tests._test_types_collections import TestCollectionsGuarantee

# TODO(snimu) include tests for 'callback' in all TestCases
# TODO(snimu) test collections
# TODO(snimu) implement enforcement & tests for binary types


if __name__ == '__main__':
    unittest.main()
