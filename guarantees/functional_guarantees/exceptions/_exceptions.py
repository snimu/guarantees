from ._util import construct_err_str
from guarantees import severity


class ParameterGuaranteesValueError(ValueError):
    def __init__(
            self,
            function_name="",
            function_namespace="",
            guarantee_name="",
            parameter_name="",
            error_severity=severity.ERROR,
            what_dict=None
    ) -> None:
        self.function_name = function_name
        self.function_namespace = function_namespace
        self.guarantee_name = guarantee_name
        self.parameter_name = parameter_name
        self.error_severity = error_severity
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            function_name=function_name,
            function_namespace=function_namespace,
            guarantee_name=guarantee_name,
            parameter_name=parameter_name,
            error_severity=error_severity,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class ParameterGuaranteesTypeError(TypeError):
    def __init__(
            self,
            function_name="",
            function_namespace="",
            guarantee_name="",
            parameter_name="",
            error_severity=severity.ERROR,
            what_dict=None
    ) -> None:
        self.function_name = function_name
        self.function_namespace = function_namespace
        self.guarantee_name = guarantee_name
        self.parameter_name = parameter_name
        self.error_severity = error_severity
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            function_name=function_name,
            function_namespace=function_namespace,
            guarantee_name=guarantee_name,
            parameter_name=parameter_name,
            error_severity=error_severity,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class ReturnGuaranteesValueError(ValueError):
    def __init__(
            self,
            function_name="",
            function_namespace="",
            guarantee_name="",
            parameter_name="return",
            error_severity=severity.ERROR,
            what_dict=None
    ) -> None:
        self.function_name = function_name
        self.function_namespace = function_namespace
        self.guarantee_name = guarantee_name
        parameter_name = "return"
        self.parameter_name = parameter_name
        self.error_severity = error_severity
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            function_name=function_name,
            function_namespace=function_namespace,
            guarantee_name=guarantee_name,
            parameter_name=parameter_name,
            error_severity=error_severity,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class ReturnGuaranteesTypeError(TypeError):
    def __init__(
            self,
            function_name="",
            function_namespace="",
            guarantee_name="",
            parameter_name="return",
            error_severity=severity.ERROR,
            what_dict=None
    ) -> None:
        self.function_name = function_name
        self.function_namespace = function_namespace
        self.guarantee_name = guarantee_name
        parameter_name = "return"
        self.parameter_name = parameter_name
        self.error_severity = error_severity
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            function_name=function_name,
            function_namespace=function_namespace,
            guarantee_name=guarantee_name,
            parameter_name=parameter_name,
            error_severity=error_severity,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class FunctionalGuaranteesUserValueError(ValueError):
    def __init__(
            self,
            function_name="",
            function_namespace="",
            guarantee_name="",
            parameter_name="",
            error_severity=severity.ERROR,
            what_dict=None
    ) -> None:
        self.function_name = function_name
        self.function_namespace = function_namespace
        self.guarantee_name = guarantee_name
        self.parameter_name = parameter_name
        self.error_severity = error_severity
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            function_name=function_name,
            function_namespace=function_namespace,
            guarantee_name=guarantee_name,
            parameter_name=parameter_name,
            error_severity=error_severity,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class FunctionalGuaranteesUserTypeError(TypeError):
    def __init__(
            self,
            function_name="",
            function_namespace="",
            guarantee_name="",
            parameter_name="",
            error_severity=severity.ERROR,
            what_dict=None
    ) -> None:
        self.function_name = function_name
        self.function_namespace = function_namespace
        self.guarantee_name = guarantee_name
        self.parameter_name = parameter_name
        self.error_severity = error_severity
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            function_name=function_name,
            function_namespace=function_namespace,
            guarantee_name=guarantee_name,
            parameter_name=parameter_name,
            error_severity=error_severity,
            what_dict=what_dict
        )
        super().__init__(self.err_str)
