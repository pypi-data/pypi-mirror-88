#!/usr/bin/env python3

from abc import ABC, abstractmethod


class MessageDelegate(ABC):

    @abstractmethod
    def name(self) -> str:
        ...
