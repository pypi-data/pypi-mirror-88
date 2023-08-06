#!/usr/bin/env python3

class NotFoundError(Exception):
    pass


class ExistedError(Exception):
    pass


class NoLayerFoundError(NotFoundError):
    pass


class LayerExistedError(ExistedError):
    pass


class NoActiveLayerError(NotFoundError):
    pass


class NoStateFoundError(NotFoundError):
    pass


class StateExistedError(ExistedError):
    pass


class NoTransitionFoundError(NotFoundError):
    pass


class TransitionExistedError(ExistedError):
    pass


class NoParameterFoundError(NotFoundError):
    pass


class ParameterExistedError(ExistedError):
    pass


class ScheduleError(Exception):
    pass


class CommandError(Exception):
    pass


class TypeLookupError(LookupError):
    pass


class ExpressionValidationError(SyntaxError):
    pass
