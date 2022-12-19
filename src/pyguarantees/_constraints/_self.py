from dataclasses import dataclass
from ._no_op import _NoOp


@dataclass
class _Self(_NoOp):
    def __post_init__(self):
        self.guarantee_name = "Self"
        self.guaranteed_type = None
