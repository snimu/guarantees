from ._util import construct_err_str


class ParameterGuaranteesValueError(ValueError):
    def __init__(
            self,
            function="",
            namespace="",
            parameter_name="",
            what_dict=None
    ) -> None:
        self.function = function
        self.namespace = namespace
        self.parameter_name = parameter_name
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            function=function,
            namespace=namespace,
            parameter_name=parameter_name,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class ParameterGuaranteesTypeError(TypeError):
    def __init__(
            self,
            function="",
            namespace="",
            parameter_name="",
            what_dict=None
    ) -> None:
        self.function = function
        self.namespace = namespace
        self.parameter_name = parameter_name
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            function=function,
            namespace=namespace,
            parameter_name=parameter_name,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class ReturnGuaranteesValueError(ValueError):
    def __init__(
            self,
            function="",
            namespace="",
            what_dict=None
    ) -> None:
        self.function = function
        self.namespace = namespace
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            function=function,
            namespace=namespace,
            parameter_name=None,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class ReturnGuaranteesTypeError(TypeError):
    def __init__(
            self,
            function="",
            namespace="",
            what_dict=None
    ) -> None:
        self.function = function
        self.namespace = namespace
        self.what_dict = what_dict
        self.err_str = construct_err_str(
            function=function,
            namespace=namespace,
            parameter_name=None,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class FunctionalGuaranteesUserValueError(ValueError):
    def __init__(
            self,
            function="",
            namespace="",
            internal_parameter_name="",
            what_dict=None
    ) -> None:
        self.function = function
        self.namespace = namespace
        self.what_dict = what_dict
        self.internal_parameter_name = internal_parameter_name
        self.err_str = construct_err_str(
            function=function,
            namespace=namespace,
            parameter_name=internal_parameter_name,
            what_dict=what_dict
        )
        super().__init__(self.err_str)


class FunctionalGuaranteesUserTypeError(TypeError):
    def __init__(
            self,
            function="",
            namespace="",
            internal_parameter_name="",
            what_dict=None
    ) -> None:
        self.function = function
        self.namespace = namespace
        self.what_dict = what_dict
        self.internal_parameter_name = internal_parameter_name
        self.err_str = construct_err_str(
            function=function,
            namespace=namespace,
            parameter_name=internal_parameter_name,
            what_dict=what_dict
        )
        super().__init__(self.err_str)
