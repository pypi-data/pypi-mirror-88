#!/usr/bin/env python3

from libLemon.MTP import Payload

class ParamGetRequestMessage(Payload):
    name: str
    typee: str
    
