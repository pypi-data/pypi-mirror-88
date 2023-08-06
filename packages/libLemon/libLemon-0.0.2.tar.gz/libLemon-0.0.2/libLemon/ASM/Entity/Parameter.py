#!/usr/bin/env python3


class ASMParameter:
    typee: type
    name: str
    value = None

    def __init__(self, typee: type, name: str, value):
        self.typee = typee
        self.name = name
        self.value = typee(value)
