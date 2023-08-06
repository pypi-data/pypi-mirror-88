#!/usr/bin/env python3

from libLemon.MTP import Payload

class ScheduleMessage(Payload):
    request: bool
    response: bool