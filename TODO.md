## Immediate steps

1. Move all TODOs here

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
  - To create `Guarantee` / enforcement-fct:
  ```python
  try:
      import torch
      # implement here
  except ImportError:
      pass 
  ```
  
  - To add to `guarantee_enforcer_mapping`-dict: 
  ```python 
  try:
    from guarantees.functional_guarantees import IsTorchTensor
    from ._enforce_torch import enforce_torchtensor
    guarantee_enforcer_mapping[IsTorchTensor] = enforce_torchtensor
  except ImportError:
    pass
  ``` 
  
  - Stuff like this should probably be put into its own function
    (`enable_third_party_library_guarantees` or something like it)
- Dynamic guarantees for other languages
  - One branch per language
  - `main`-branch just has some description & examples
  - Each other branch named after its language (`python`, `Cpp`, ...)