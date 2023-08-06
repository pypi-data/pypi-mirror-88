#!/usr/bin/env python3

from abc import ABC, abstractmethod

import paho.mqtt.client as mqtt

import libLemon.Utils.Args as Args
from libLemon.Utils.Const import SCHEDULE_REQUEST_MESSAGE, SCHEDULE_RESPONSE_MESSAGE, YIELD_MESSAGE, LEFT_ARROW, RIGHT_ARROW


class ASMKernel(ABC):
    name: str
    exec_path: str
    layer_name: str
    activated: bool
    client: mqtt.Client

    def on_message(self, client: mqtt.Client, userdata, msg):
        if msg.payload.decode() == SCHEDULE_REQUEST_MESSAGE:
            self.activated = True

    def __init__(self):
        host = Args.get_arg_str('host')
        port = Args.get_arg_int('port')

        self.activated = False
        self.name = Args.get_arg_str('kernel_name')
        self.layer_name = Args.get_arg_str('layer_name')
        self.exec_path = Args.get_filename()
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(host, port, 600)  # 600为keepalive的时间间隔
        self.client.subscribe(RIGHT_ARROW.join(
            [self.layer_name, self.name]), qos=0)
        self.client.loop_start()

    @abstractmethod
    def kernel_init(self):
        pass

    def _kernel_awake(self):
        while not self.activated:
            pass
        self.client.publish(
            LEFT_ARROW.join([self.layer_name, self.name]), payload=SCHEDULE_RESPONSE_MESSAGE, qos=0)

    @abstractmethod
    def kernel_workload(self):
        pass

    def _kernel_yield(self):
        self.activated = False
        self.client.publish(
            LEFT_ARROW.join([self.layer_name, self.name]), payload=YIELD_MESSAGE, qos=0)

    def start(self):
        self.kernel_init()
        while True:
            self._kernel_awake()
            self.kernel_workload()
            self._kernel_yield()
