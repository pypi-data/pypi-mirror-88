#!/usr/bin/env python3

from libLemon.MTP import Payload
from libLemon.ASM.Message.ScheduleRequestMessage import ScheduleRequestMessage

class ScheduleResponseMessage(Payload):
    request: ScheduleRequestMessage
    status: str