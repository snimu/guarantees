from dataclasses import dataclass
from ._base import _Guarantee


@dataclass
class _NoOp(_Guarantee):
    def __post_init__(self):
        self.guarantee_name = "NoOp"
        self.guaranteed_type = None

    def enforce(self, arg):
        return arg
