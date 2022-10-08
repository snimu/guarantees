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

# TODO: test_mixed_arg_kwarg in _test_parameters_guarantee_common

# TODO (snimu) "types" parameter in collections -> if not None, check (with any)
#   that all members of the collectible are of the type
#   ("key_types", "val_types" for dict; "types" checks both here)

# TODO (snimu)
#  - IsNumpyArray (valid_shapes)
#  - IsTorchTensor (valid_shapes, valid_devices)

# TODO (snimu) Create (and only raise) custom Exceptions
#   - Change existing documentation accordingly
#   - Write documentation for the decorators (specifically `add_guarantees`)

# TODO (snimu) guarantee tests

# TODO (snimu) dynamic guarantees for other languages: Rust, C++, Java, etc.
#   -> one branch per language.
#   Subbranches in naming style: <language>-<branch>


if __name__ == '__main__':
    unittest.main()
    test_onoff()
