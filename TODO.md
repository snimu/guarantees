# TODO: both

- Ensure that everything is thread-save.
- Docstrings!!!
- Make `severity` part of `functional_guaranatees`

# TODO: `functional_guarantees`

- README: explain how severity allows to treat things like using the default value as a warning but a problem with 
the actual argument as an error &rarr; example: default `None` but should be `list` &rarr; warn when using `None`

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

- make it work with functions nested inside of methods
- Make it independent of the `unittest`-framework
  - Can in principle decorate any function
  - Make `enforce` independent of framework&mdash;just call it after you've run your tests.
- More tests
- write plenty of comments so that my reasoning is understandable 
   (or I won't understand the code soon)
- Make `enforce` and `main` take more arguments, so that they can be used more 
flexibly (like `unittest.main`).