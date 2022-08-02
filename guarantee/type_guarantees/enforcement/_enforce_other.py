import warnings

from guarantee.type_guarantees.guarantees import IsClass
from guarantee.type_guarantees.signals.base import SignalTypeError


# NoOp needs no enforcement; it is handled in the guarantee_handler
def enforce_isclass(arg: object, guarantee: IsClass) -> object:
    arg = _check_type(arg, guarantee)
    if guarantee.check_fct is not None:
        return guarantee.check_fct(arg)
    return arg


def _check_type(arg: object, guarantee: IsClass) -> object:
    if guarantee.class_type is None:
        err_msg = "You tried to enforce a class type but class_type is None. "
        if guarantee.warnings_only:
            warnings.warn(err_msg + "Ignoring.")
        else:
            raise TypeError(err_msg)

    if not isinstance(arg, guarantee.class_type):
        if guarantee.callback is not None:
            guarantee.callback(
                SignalTypeError(
                    arg_name=guarantee.name,
                    type_should=str(type(guarantee.class_type)),
                    type_is=str(type(arg)),
                    force_conversion=False
                )
            )
        else:
            err_msg = f"Guaranteed type {guarantee.class_type} " \
                      f"for parameter {guarantee.name}, " \
                      f"but received type {type(arg)}. " \
                      f"force_conversion parameter ignored. "
            if guarantee.warnings_only:
                warnings.warn(err_msg)
            else:
                raise TypeError(err_msg)

    return arg
