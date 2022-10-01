from ._util import construct_err_str


class ParameterGuaranteesValueError(ValueError):
    def __init__(
            self,
            function_name="",
            function_namespace="",
            parameter_name="",
            guarantee_type_name="",
            what_dict=None
    ) -> None:
        self.function_name = function_name
        self.function_namespace = function_namespace
        self.parameter_name = parameter_name
        self.guarantee_type_name = guarantee_type_name
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            function_name=function_name,
            function_namespace=function_namespace,
            parameter_name=parameter_name,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class ParameterGuaranteesTypeError(TypeError):
    def __init__(
            self,
            function_name="",
            function_namespace="",
            parameter_name="",
            guarantee_type_name="",
            what_dict=None
    ) -> None:
        self.function_name = function_name
        self.function_namespace = function_namespace
        self.parameter_name = parameter_name
        self.guarantee_type_name = guarantee_type_name
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            function_name=function_name,
            function_namespace=function_namespace,
            parameter_name=parameter_name,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class ReturnGuaranteesValueError(ValueError):
    def __init__(
            self,
            function_name="",
            function_namespace="",
            guarantee_type_name="",
            what_dict=None
    ) -> None:
        self.function_name = function_name
        self.function_namespace = function_namespace
        self.guarantee_type_name = guarantee_type_name
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            function_name=function_name,
            function_namespace=function_namespace,
            parameter_name=None,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class ReturnGuaranteesTypeError(TypeError):
    def __init__(
            self,
            function_name="",
            function_namespace="",
            guarantee_type_name="",
            what_dict=None
    ) -> None:
        self.function_name = function_name
        self.function_namespace = function_namespace
        self.guarantee_type_name = guarantee_type_name
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            function_name=function_name,
            function_namespace=function_namespace,
            parameter_name=None,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class FunctionalGuaranteesUserValueError(ValueError):
    def __init__(
            self,
            function_name="",
            function_namespace="",
            internal_parameter_name="",
            guarantee_type_name="",
            what_dict=None
    ) -> None:
        self.function_name = function_name
        self.function_namespace = function_namespace
        self.internal_parameter_name = internal_parameter_name
        self.guarantee_type_name = guarantee_type_name
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            function_name=function_name,
            function_namespace=function_namespace,
            parameter_name=internal_parameter_name,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class FunctionalGuaranteesUserTypeError(TypeError):
    def __init__(
            self,
            function_name="",
            function_namespace="",
            internal_parameter_name="",
            guarantee_type_name="",
            what_dict=None
    ) -> None:
        self.function_name = function_name
        self.function_namespace = function_namespace
        self.guarantee_type_name = guarantee_type_name
        self.internal_parameter_name = internal_parameter_name
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            function_name=function_name,
            function_namespace=function_namespace,
            parameter_name=internal_parameter_name,
            what_dict=what_dict
        )
        super().__init__(self.err_str)
