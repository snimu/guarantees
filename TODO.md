## Immediate steps

0. Move all TODOs here

1. Create `util`&ndash;directory.
    - `util.typenames` or something like it
    - `util.error_handeling`
    - `util.other`
   
2. Change `check_fct`&ndash;member for `TypeGuarantee`s.
   - `guarantee.check_functions`
     - Example:
         ````python
         fg.add_guarantees(
            ...,
            parameter_guarantees=[
                fg.IsInt(
                    "a",
                    check_functions=[
                        [lambda x: x % 3 == 0, "divisible by 3"],
                        lambda x: x in [1, 2, 3]
                    ]               
                )
            ]
         )
         def fct(a):
            pass
         ````
   - List of functions of the signature:
     ````python
     def function(arg: <guaranteed-type>) -> bool:
        ...
     ````
   - Put a function that checks these functions into `util.something`
     ````python
     # TODO: find some way to include the associated error-messages
     errors = []
     for i, f in enumerate(guarantee.check_functions):
        if not f(arg):
            errors.append(i)
     
     if errors:
        what_dict = {
            "error": "violated ...", 
            "arg": arg
        }
        
        for i, err_ind in enumerate(errors):
            what_dict[f"error {i}" = \
                f"....check_function[{err_ind}]: "
                f"{get_error_msg(guarantee.check_functions[err_ind])}"
        
        handle_errors(
            ...,
            what_dict=what_dict
        )
     ````

## Other
