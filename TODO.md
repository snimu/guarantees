## Immediate steps

1. Make sure that `functional_guarantees` work with methods; especially `self`
   might be an issue, as well as `cls` for a `classmethod`.

2. Save arg in Exceptions
    - add `arg` to Exception arguments
    - add `self.arg` in all Exceptions

## Other

- `description`-parameter?

- test_mixed_arg_kwarg in _test_parameters_guarantee_common

- In `CollectionType`: `types`-member
  - Is list of more Guarantees
  - For dict: has `key_types` and `val_types`, where `types` checks both
  
- Guarantees for types from package `collections` 
  - Just add those to `_collections.py`

- Support for third-party libraries
  - Examples:
    - `IsNumpyArray`
    - `IsTorchTensor`
  - Some way to easily extend this library with ever-more types
    - IMPORTANT: Rewrite below

- Rewrite: Add method `Guarantee.enforce(value)`
  - Can put `_enforce_isunion` out of the `_guarantee_handler.py`
  - Is more readable
  - Can more easily extend the library

- Dynamic guarantees for other languages
  - One branch per language
  - `main`-branch just has some description & examples
  - Each other branch named after its language (`python`, `Cpp`, ...)