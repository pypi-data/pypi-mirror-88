#!/usr/bin/env python3

import threading
from typing import Type

from libLemon.ASM.Entity import ASMLayer, ASMParameter
from libLemon.ASM.Delegate import ParamDelegate
from libLemon.Error import NoLayerFoundError, LayerExistedError, NoParameterFoundError, ParameterExistedError

_global_asm = None


class ASMMain(ParamDelegate):
    _layers: dict[str: ASMLayer]
    _parameters: dict[str: ASMParameter]

    def __init__(self, layers: list[ASMLayer] = list(), params: list[ASMParameter] = list()):
        self._layers = {layer.name: layer for layer in layers}
        self._parameters = {params.name: params for params in params}

    """
    layer getter/setter methods
    """

    def add_layer(self, layer: ASMLayer):
        if layer.name in self._layers:
            raise LayerExistedError('existed layer named `%s`' % layer.name)
        self._layers.update({layer.name: layer})

    def get_layer(self, name: str) -> ASMLayer:
        try:
            return self._layers[name]
        except KeyError:
            raise NoLayerFoundError('no layer named `%s`' % name)

    def del_layer(self, name: str):
        try:
            del self._layers[name]
        except KeyError:
            raise NoLayerFoundError('no layer named `%s`' % name)

    def get_all_layers(self) -> list[ASMLayer]:
        return [layer for _, layer in self._layers.items()]

    def del_all_layers(self):
        self._layers.clear()

    """
    param getter/setter methods
    """

    def add_param(self, param: ASMParameter):
        if param.name in self._parameters:
            raise ParameterExistedError(
                'existed parameter named `%s`' % param.name)
        self._parameters.update({param.name: param})

    def get_param(self, name: str) -> ASMParameter:
        try:
            return self._parameters[name]
        except KeyError:
            raise NoParameterFoundError('no param named `%s`' % name)

    def del_param(self, name: str):
        try:
            del self._parameters[name]
        except KeyError:
            raise NoParameterFoundError('no param named `%s`' % name)

    def get_all_params(self) -> list[ASMParameter]:
        return [param for _, param in self._parameters.items()]

    def del_all_params(self):
        self._parameters.clear()

    """
    ParamDelegate methods
    """

    def get_parameter_value(self, name: str):
        try:
            return self._parameters[name].value
        except KeyError:
            raise NoParameterFoundError('failed to get parameter named `%s`' % name)

    def get_all_params_name(self) -> list[str]:
        return [name for name, _ in self._parameters.items()]

    def set_parameter_value(self, name: str, value):
        try:
            if self._parameters[name].typee == type(value):
                self._parameters[name].value = value
            else:
                raise TypeError('type mismatch for parameter named `%s` (got %s, expected %s)' % (name, type(value), self._parameters[name].typee))
        except KeyError:
            raise NoParameterFoundError('failed to get parameter named `%s`' % name)

    def start(self):
        for _, layer in self._layers.items():
            threading.Thread(target=lambda: layer.start()).start()


def get_asm() -> ASMMain:
    global _global_asm
    if not _global_asm:
        _global_asm = ASMMain()
    return _global_asm
