# Package: guarantee

A package for dynamically enforcing guarantees.

## Package layout

All inside PyCharm project guarantees

- guarantee (the package)
    - \_\_init\_\_.py   (import all user-facing things)
    - exceptions
      - \_\_init\_\_.py
      - exceptions.py
      - signals.py
    - type_guarantees
      - guarantees
      - error_checking
      - error_handling
    - test_guarantees
- tests (testing)


## Type guarantees

### The guarantees

- Binary types
  - bytes
  - bytearray
  - memoryview
- Boolean type
  - bool
- Collections
  - list
  - tuple
  - dict
  - set
  - frozenset
  - range
- Numeric types
  - int
  - float
  - complex
- Text type
  - str
- Other
  - noop

### Their parameters

**All** have the `name` parameter.

Unless specified otherwise, all have the `warnings_only` 
and the `force_conversion` parameters.

#### Numeric types

| type &darr; param &rarr; | isin | minimum | maximum | minimum_re | minimum_im | maximum_re | maximum_im |
|:-------------------------|:----:|:-------:|:-------:|:----------:|:----------:|:----------:|:----------:|
| isint                    |  y   |    y    |    y    |     n      |     n      |     n      |     n      |
| isfloat                  |  y   |    y    |    y    |     n      |     n      |     n      |     n      |
| iscomplex                |  y   |    y    |    y    |     y      |     y      |     y      |     y      |

#### Collections

| type &darr; param &rarr; | contains | has_keys | has_values | minimum_len | maximum_len |
|:-------------------------|:--------:|:--------:|:----------:|:-----------:|:-----------:|
| islist                   |    y     |    n     |     n      |      y      |      y      |
| istuple                  |    y     |    n     |     n      |      y      |      y      |
| isdict                   |    n     |    y     |     y      |      y      |      y      |
| isrange                  |    ?     |    n     |     n      |      ?      |      ?      |
| isset                    |    y     |    n     |     n      |      y      |      y      |
| isfrozenset              |    y     |    n     |     n      |      y      |      y      |


#### String types

| type &darr; param &rarr; | minimum_len | maximum_len |
|:-------------------------|:-----------:|:-----------:|
| isstr                    |      y      |      y      |

#### Boolean types

| type &darr; param &rarr; | 
|:-------------------------|
| isbool                   |

#### Binary types

| type &darr; param &rarr; |
|:-------------------------|
| isbytes                  |
| isbytearray              |
| ismemoryview             |

#### Other 

| type &darr; param &rarr; | check_fct | class_type |
|:-------------------------|:---------:|:----------:|
| noop                     |     n     |     n      |
| isclass                  |     y     |     y      |

`noop` does not contain `force_conversion` or `warnings_only`!


