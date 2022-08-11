import unittest

# Import unittest from their respective files
#   -> unittest.main() will run them all
from tests._test_types_numeric import TestNumericGuarantee
from tests._test_types_string import TestStringGuarantee
from tests._test_types_boolean import TestBooleanGuarantee
from tests._test_types_other import TestOther
from tests._test_types_collections import TestCollectionsGuarantee

# TODO (snimu) Rename 'guarantee' to 'guarantees' (mirror repo name)

# TODO (snimu) include tests for 'callback' in all TestCases

# TODO (snimu) implement enforcement & tests for binary types

# TODO (snimu) improve error messages

# TODO (snimu) instead of finding out the type_str manually every time,
#   make fcts 'type_from_guarantee' and 'type_name_from_guarantee'

# TODO (snimu) make more use of _util everywhere -> nicer error msgs, etc.

# TODO (snimu) "const" parameter in Guarantees?

# TODO (snimu) guarantees for return values

# TODO (snimu) guarantees for other languages: Rust, C++, Java, etc.
#   -> one branch per language.
#   Subbranches in naming style: <language>-<branch>


if __name__ == '__main__':
    unittest.main()
