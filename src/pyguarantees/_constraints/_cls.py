from dataclasses import dataclass
from ._no_op import _NoOp


@dataclass
class _Cls(_NoOp):
    def __post_init__(self):
        self.guarantee_name = "Cls"
        self.guaranteed_type = None
