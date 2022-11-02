# TODO: `functional_guarantees`

## Immediate steps

1. Make `functional_guarantees` work properly with `staticmethod`s
    - Might have to add a `staticmethod`-member to `Guarantee`

2. Move each class in `_other.py` into its own file for clarity
    - Same for tests

3. Save arg in Exceptions
    - add `arg` to Exception arguments
    - add `self.arg` in all Exceptions

4. In `CollectionType`: `types`-member
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

## Issues

- When doing a `from x import y`, 

## Design

- At the end of a file, use `guarantee_tests_for(functions: List[callable])`