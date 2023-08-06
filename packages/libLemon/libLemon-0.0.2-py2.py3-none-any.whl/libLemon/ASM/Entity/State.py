#!/usr/bin/env python3


from time import sleep


import libLemon.Utils.Logger as Logger
from libLemon.MTP import EMQ, Messenger
from libLemon.Utils.Runner import run_module
from libLemon.ASM.Message.YieldMessage import YieldMessage
from libLemon.ASM.Message.ScheduleMessage import ScheduleMessage
from libLemon.Utils.Const import ASM_NAME_PREFIX, MODULE_NAME_PREFIX, SCHEDULE_REQUEST_MESSAGE, SCHEDULE_RESPONSE_MESSAGE, YIELD_MESSAGE


class ASMState:

    name: str
    exec_path: str
    layer_name: str

    _activated: bool
    _messenger: Messenger

    def __init__(self, layer_name: str, name: str, exec_path: str):
        self.layer_name = layer_name
        self.name = name
        self.exec_path = exec_path

    def __str__(self) -> str:
        return 'ASMState `%s` (%s): %s' % (self.name, self.layer_name, self.exec_path)

    def _schedule_response_received(self, payload: ScheduleMessage):
        assert(not payload.request)
        assert(payload.response)
        self._activated = True

    
    def _yield_received(self, _: YieldMessage):
        self._activated = False

    def start(self):
        """
        install asm kernel module
        """
        self._activated = False

        self._messenger = Messenger(ASM_NAME_PREFIX + self.layer_name, MODULE_NAME_PREFIX + self.name)
        self._messenger.install_callback(ScheduleMessage, self._schedule_response_received)
        self._messenger.install_callback(YieldMessage, self._yield_received)

        host, port = EMQ.get_addr()
        run_module(self.exec_path, params={
            'emq_host': host,
            'emq_port': port,
            'kernel_name': self.name,
            'layer_name': self.layer_name})

    def schedule(self):  # 调度
        # block until ASMKernel returns or dies

        while not self._activated:
            self._messenger.publish(ScheduleMessage(request=True, response=False))
            sleep(0.1)

        Logger.info('activated')
        while self._activated:
            pass

        Logger.info('yield!')

    def is_running(self) -> bool:
        return self._activated
