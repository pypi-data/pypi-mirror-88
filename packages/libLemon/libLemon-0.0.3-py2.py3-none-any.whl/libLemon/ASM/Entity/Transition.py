#!/usr/bin/env python3


class ASMTransition:
    name: str
    from_state: str
    to_state: str
    condition: str
    priority: int

    def __init__(self, name: str, from_state: str, to_state: str, condition: str, priority: int):
        self.name = name
        self.from_state = from_state
        self.to_state = to_state
        self.condition = condition
        self.priority = priority

    def __str__(self) -> str:
        return 'ASMTransition `%s`: %s => %s when `%s`, at priority #%d' % (self.name, self.from_state, self.to_state, self.condition, self.priority)
