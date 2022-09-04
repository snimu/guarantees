import unittest

# Import unittest from their respective files
#   -> unittest.main() will run them all
from tests._test_parameters_numeric import TestNumericGuarantee
from tests._test_parameters_string import TestStringGuarantee
from tests._test_parameters_boolean import TestBooleanGuarantee
from tests._test_parameters_other import TestIsClass, TestIsNone, TestIsUnion
from tests._test_parameters_collections import TestCollectionsGuarantee
from tests._test_parameters_common import TestCallback, test_onoff
from tests._test_parameters_binary import TestBinary
from tests._test_return_guarantees import TestReturnGuarantees

# TODO (snimu) "description" parameter?

# TODO (snimu) Write docstrings

# TODO (snimu) classes for return values

# TODO (snimu) guarantee tests

# TODO (snimu) classes for other languages: Rust, C++, Java, etc.
#   -> one branch per language.
#   Subbranches in naming style: <language>-<branch>


if __name__ == '__main__':
    unittest.main()
    test_onoff()
