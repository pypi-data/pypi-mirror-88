#!/usr/bin/env python3

from abc import ABC, abstractmethod

import paho.mqtt.client as mqtt
from libLemon.ASM.Message.ScheduleMessage import ScheduleMessage
from libLemon.ASM.Message.YieldMessage import YieldMessage
from libLemon.MTP import EMQ
from libLemon.MTP.Messenger import Messenger

import libLemon.Utils.Args as Args
from libLemon.Utils.Const import ASM_NAME_PREFIX, MODULE_NAME_PREFIX, SCHEDULE_REQUEST_MESSAGE, SCHEDULE_RESPONSE_MESSAGE, YIELD_MESSAGE, LEFT_ARROW, RIGHT_ARROW


class ASMKernel(ABC):

    name: str
    exec_path: str
    layer_name: str

    _activated: bool
    _messenger: Messenger

    def __init__(self):        
        self.name = Args.get_arg_str('kernel_name')
        self.layer_name = Args.get_arg_str('layer_name')
        self.exec_path = Args.get_filename()
        self.host, self.port = EMQ.get_addr()

    @abstractmethod
    def kernel_init(self):
        pass

    @abstractmethod
    def kernel_workload(self):
        pass

    def _kernel_awake(self):
        while not self._activated:
            pass
        self._messenger.publish(ScheduleMessage(request=False, response=True))

    def _kernel_yield(self):
        self._activated = False
        self._messenger.publish(YieldMessage())

    def _schedule_request_received(self, payload: ScheduleMessage):
        assert(payload.request)
        assert(not payload.response)
        self._activated = True

    def start(self):
        self._activated = False
        self._messenger = Messenger(MODULE_NAME_PREFIX + self.name, ASM_NAME_PREFIX + self.layer_name)
        self._messenger.install_callback(ScheduleMessage, self._schedule_request_received)
        self.kernel_init()
        while True:
            self._kernel_awake()
            self.kernel_workload()
            self._kernel_yield()
