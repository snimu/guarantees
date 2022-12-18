# TODO: both

- Ensure that everything is thread-save.
- Improve test-coverage
- Docstrings!!!
- VSCode Plugin for syntax highlighting setting the `pg`-decorators apart from regular code
- Good build system
  - Upload to PyPI
  - Upload to Conda
  - Make Docker Image
  - Add wheels
- Version Numbers:
  - 1.x.x only when
    - No more API changes
    - Documentation & build system & git page at acceptable level

# TODO: `testcase`

- `GuaranteeInternal` for giving `handle_error` when another guarantee is inappropriate

- Move each class in `_other.py` into its own file for clarity
    - Same for tests

- Save arg in Exceptions
    - add `arg` to Exception arguments
    - add `self.arg` in all Exceptions

- In `CollectionType`: `types`-member
  - Is list of more Guarantees
  - For dict: has `key_types` and `val_types`, where `types` checks both

- `description`-parameter?

- Guarantees for types from package `collections` 
  - Just add those to `_collections.py`

- Support for third-party libraries (a.k.a. `IsTorchTensor` or `IsNumpyArray` or `IsDataFrame`)

- Dynamic guarantees for other languages
  - One branch per language
  - `main`-branch just has some description & examples
  - Each other branch named after its language (`python`, `Cpp`, ...)


# TODO: `testcase`

- make it work with functions nested inside of methods
- More tests
- Make `enforce` and `main` take more arguments, so that they can be used more 
flexibly (like `unittest.main`).