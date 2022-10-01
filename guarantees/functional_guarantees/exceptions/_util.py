def _parse_what_dict(what_dict: dict, tabs: str = "\t") -> str:
    err_str = ""
    for key, val in what_dict.items():
        if type(val) is dict:
            err_str += f"{tabs}key: \n"
            err_str += _parse_what_dict(val, tabs + "\t")
        else:
            err_str += f"{tabs}{key}: {val} \n"

    return err_str


def construct_err_str(
        function_name: str,
        function_namespace: str,
        guarantee_name: str,
        what_dict: dict = None
) -> str:
    err_str = f"\nWhere: {function_namespace}.{function_name} \n"
    err_str += f"\tGuarantee: {guarantee_name} \n"
    err_str += _parse_what_dict(what_dict)
    return err_str
