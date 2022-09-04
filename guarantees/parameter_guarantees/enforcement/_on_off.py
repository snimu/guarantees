from guarantees.parameter_guarantees.enforcement._guarantee_handler import \
    ParameterHandler


class OnOff:
    on = True


def on():
    OnOff.on = True


def off():
    OnOff.on = False
    ParameterHandler.handles = {}
