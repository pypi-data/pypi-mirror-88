#!/usr/bin/env python3

class NotFoundError(Exception):
    ...


class ExistedError(Exception):
    ...


class NoLayerFoundError(NotFoundError):
    ...


class LayerExistedError(ExistedError):
    ...


class NoActiveLayerError(NotFoundError):
    ...


class NoStateFoundError(NotFoundError):
    ...


class StateExistedError(ExistedError):
    ...


class NoTransitionFoundError(NotFoundError):
    ...


class TransitionExistedError(ExistedError):
    ...


class NoParameterFoundError(NotFoundError):
    ...


class ParameterExistedError(ExistedError):
    ...


class ScheduleError(Exception):
    ...


class CommandError(Exception):
    ...


class TypeLookupError(LookupError):
    ...


class ExpressionValidationError(SyntaxError):
    ...

class SerializeError(Exception):
    ...
    
class DeserializeError(Exception):
    ...

class NoTypeFoundError(DeserializeError):
    ...

class EMQInitError(Exception):
    ...