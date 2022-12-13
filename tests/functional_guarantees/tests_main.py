import unittest

# Import unittest from their respective files
#   -> unittest.main() will run them all
from tests.functional_guarantees._test_numeric import TestNumericGuarantee
from tests.functional_guarantees._test_string import TestStringGuarantee
from tests.functional_guarantees._test_boolean import TestBooleanGuarantee
from tests.functional_guarantees._test_collections import TestCollectionsGuarantee
from tests.functional_guarantees._test_common import TestCallback, TestCheckFunctions,\
    TestMethodGuarantees, TestReturnGuarantees, TestLogger, TestParameterMatching, \
    TestForbiddenValues
from tests.functional_guarantees._test_binary import TestBinary
from tests.functional_guarantees._test_onoff import test_onoff


if __name__ == '__main__':
    unittest.main(exit=False)
    test_onoff()
