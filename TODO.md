# TODO: both

- Ensure that everything is thread-save.
- Docstrings!!!

# TODO: `functional_guarantees`

- Redesign `check_functions`:
  - Should have clearer interface.
  - For example: be given a class `fg.DynamicCheck(check: callable, error_handler: callable = None, description: str = None)`.
  - Allows user to define the check and what happens when it fails, or the message that appears when it fails.

- Give `TypeGuarantee`s a `use_isinstance` parameter to use `isinstance(a, b)` instead of `type(a) is b`, 
which should be the default behavior.

- Move each class in `_other.py` into its own file for clarity
    - Same for tests

- Save arg in Exceptions
    - add `arg` to Exception arguments
    - add `self.arg` in all Exceptions

- In `CollectionType`: `types`-member
  - Is list of more Guarantees
  - For dict: has `key_types` and `val_types`, where `types` checks both

- `description`-parameter?

- test_mixed_arg_kwarg in _test_parameters_guarantee_common
  
- Guarantees for types from package `collections` 
  - Just add those to `_collections.py`

- Support for third-party libraries (a.k.a. `IsTorchTensor` or `IsNumpyArray` or `IsDataFrame`)

- Dynamic guarantees for other languages
  - One branch per language
  - `main`-branch just has some description & examples
  - Each other branch named after its language (`python`, `Cpp`, ...)


# TODO: `test_guarantees`

[] make it work with classmethods
[] make it work with functions nested inside of methods
- More tests
- write plenty of comments so that my reasoning is understandable 
   (or I won't understand the code soon)
- Make `enforce` and `main` take more arguments, so that they can be used more 
flexibly (like `unittest.main`).