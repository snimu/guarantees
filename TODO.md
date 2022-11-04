# TODO: `functional_guarantees`

## Immediate steps

- Move each class in `_other.py` into its own file for clarity
    - Same for tests

- Save arg in Exceptions
    - add `arg` to Exception arguments
    - add `self.arg` in all Exceptions

- In `CollectionType`: `types`-member
  - Is list of more Guarantees
  - For dict: has `key_types` and `val_types`, where `types` checks both

## Other

- `description`-parameter?

- test_mixed_arg_kwarg in _test_parameters_guarantee_common
  
- Guarantees for types from package `collections` 
  - Just add those to `_collections.py`

- Support for third-party libraries

- Dynamic guarantees for other languages
  - One branch per language
  - `main`-branch just has some description & examples
  - Each other branch named after its language (`python`, `Cpp`, ...)


# TODO: `test_guarantees`

- More tests
- write plenty of comments so that my reasoning is understandable 
   (or I won't understand the code soon)