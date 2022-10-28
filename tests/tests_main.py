import unittest

# Import unittest from their respective files
#   -> unittest.main() will run them all
from tests._test_parameters_numeric import TestNumericGuarantee
from tests._test_parameters_string import TestStringGuarantee
from tests._test_parameters_boolean import TestBooleanGuarantee
from tests._test_parameters_other import TestIsClass, TestIsNone, TestIsUnion
from tests._test_parameters_collections import TestCollectionsGuarantee
from tests._test_parameters_common import TestCallback, TestCheckFunctions,\
    test_onoff, TestMethodGuarantees
from tests._test_parameters_binary import TestBinary
from tests._test_return_guarantees import TestReturnGuarantees


if __name__ == '__main__':
    unittest.main()
    test_onoff()
