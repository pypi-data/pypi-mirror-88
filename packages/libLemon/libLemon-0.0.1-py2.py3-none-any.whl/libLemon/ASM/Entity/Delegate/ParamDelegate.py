#!/usr/bin/env python3

from abc import ABC, abstractmethod


class ParamDelegate(ABC):

    @abstractmethod
    def get_parameter_value(self, name: str):
        ...

    @abstractmethod
    def get_all_params_name(self) -> list[str]:
        ...

    @abstractmethod
    def set_parameter_value(self, name: str, value):
        ...
