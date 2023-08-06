#!/usr/bin/env python3

from time import sleep
import paho.mqtt.client as mqtt

import libLemon.Utils.Args as Args
import libLemon.Utils.Logger as Logger
from libLemon.Utils.Runner import run_module
from libLemon.Utils.Const import SCHEDULE_REQUEST_MESSAGE, SCHEDULE_RESPONSE_MESSAGE, YIELD_MESSAGE, LEFT_ARROW, RIGHT_ARROW


class ASMState:
    _layer_name: str

    name: str
    exec_path: str

    _activated: bool
    _client: mqtt.Client

    def __init__(self, layer_name: str, name: str, exec_path: str):
        self._activated = False
        self._layer_name = layer_name
        self.name = name
        self.exec_path = exec_path

    def __str__(self) -> str:
        return 'ASMState `%s` (%s): %s' % (self.name, self._layer_name, self.exec_path)

    def on_message(self, client: mqtt.Client, userdata, msg):
        Logger.info('on message! payload = %s' % msg.payload.decode())
        if msg.payload.decode() == SCHEDULE_RESPONSE_MESSAGE:
            self._activated = True
        elif msg.payload.decode() == YIELD_MESSAGE:
            self._activated = False

    def start(self):
        """
        install asm kernel module
        """
        host = Args.get_arg_str('host')
        port = Args.get_arg_int('port')

        self.process = run_module(self.exec_path, params=[
                                  '--host=%s' % host, '--port=%d' % port, '--kernel_name="%s"' % self.name, '--layer_name="%s"' % self._layer_name])
        self._client = mqtt.Client()
        self._client.on_message = self.on_message
        self._client.connect(host, port, 600)  # 600为keepalive的时间间隔
        self._client.subscribe(LEFT_ARROW.join(
            [self._layer_name, self.name]), qos=0)
        self._client.loop_start()

    def schedule(self):  # 调度
        # block until ASMKernel returns or dies

        while not self._activated:
            self._client.publish(
                RIGHT_ARROW.join([self._layer_name, self.name]), payload=SCHEDULE_REQUEST_MESSAGE, qos=0)
            sleep(0.1)

        Logger.info('activated')
        while self._activated:
            pass

        Logger.info('yield!')

    def is_running(self) -> bool:
        return self._activated
