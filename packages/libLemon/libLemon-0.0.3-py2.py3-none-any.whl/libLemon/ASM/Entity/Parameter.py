#!/usr/bin/env python3


class ASMParameter:
    typee: type
    name: str
    value = None

    def __init__(self, typee: type, name: str, value=None):
        self.typee = typee
        self.name = name

        if value != None:
            self.value = typee(value)
        else:
            self.value = None
