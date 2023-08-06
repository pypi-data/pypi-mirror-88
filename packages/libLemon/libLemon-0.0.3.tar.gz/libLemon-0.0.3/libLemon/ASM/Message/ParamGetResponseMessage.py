#!/usr/bin/env python3

from libLemon.MTP import Payload
from libLemon.ASM.Message.ParamGetRequestMessage import ParamGetRequestMessage

class ParamGetResponseMessage(Payload):
    request: ParamGetRequestMessage
    status: str
    value: str