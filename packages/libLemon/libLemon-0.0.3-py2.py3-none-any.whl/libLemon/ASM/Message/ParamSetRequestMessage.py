#!/usr/bin/env python3

from libLemon.MTP import Payload

class ParamSetRequestMessage(Payload):
    name: str
    typee: str
    value: str
