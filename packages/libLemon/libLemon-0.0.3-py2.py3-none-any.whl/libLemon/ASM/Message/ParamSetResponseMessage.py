#!/usr/bin/env python3

from libLemon.MTP import Payload
from libLemon.ASM.Message.ParamSetRequestMessage import ParamSetRequestMessage

class ParamSetResponseMessage(Payload):
    request: ParamSetRequestMessage
    status: str