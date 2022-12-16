# TODO: both

- Ensure that everything is thread-save.
- Docstrings!!!
- Make `severity` part of `functional_guarantees`
- VSCode Plugin for syntax highlighting setting the `fg`-decorators apart from regular code
- Good build system
  - Upload to PyPI
  - Upload to Conda
  - Make Docker Image
  - Add wheels
- Version Numbers:
  - 1.x.x only when
    - No more API changes
    - Documentation & build system & git page at acceptable level
  - 0.1.x only when
    - README.md version 1 finished
    - `collections` work in `fg`

# TODO: `functional_guarantees`

- Add `Guarantee` to `fg`-namespace -> can do an `isinstance` for example.

- Change `return_guarantee` to `return_guarantees` -> when you do something like `return a, b, c`
  - Advantage: Clearer.
  - Can still guarantee several `tuple` values (or a `tuple` and some other values).
  - Point is: Gives more flexibility *and* works while `CollectionType`-guarantees dont't have a `types`-member.

- README: explain how severity allows to treat things like using the default value as a warning but a problem with 
the actual argument as an error &rarr; example: default `None` but should be `list` &rarr; warn when using `None`

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