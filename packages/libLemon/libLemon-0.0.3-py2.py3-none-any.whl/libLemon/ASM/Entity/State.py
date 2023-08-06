#!/usr/bin/env python3


import subprocess

import libLemon.Utils.Logger as Logger
from libLemon.MTP import EMQ, Messenger
from libLemon.Utils.Runner import run_module
from libLemon.ASM.Delegate import ParamDelegate
from libLemon.ASM.Message import ParamSetRequestMessage, ParamGetRequestMessage, ParamGetResponseMessage, ParamSetResponseMessage, ScheduleRequestMessage, ScheduleResponseMessage, YieldMessage
from libLemon.Utils.Utilities import str2typ
from libLemon.Utils.Const import ASM_NAME_PREFIX, MODULE_NAME_PREFIX, STATUS_BAD_TYPE, STATUS_NO_PARAM, STATUS_OK
from libLemon.Utils.Sleep import sleep
from libLemon.Error import NoParameterFoundError

class ASMState:

    name: str
    exec_path: str
    layer_name: str

    _delegate: ParamDelegate

    _started: bool = False
    _activated: bool = False
    _messenger: Messenger = None
    _popen: subprocess.Popen = None

    def __init__(self, layer_name: str, name: str, exec_path: str, delegate: ParamDelegate = None):
        self.layer_name = layer_name
        self.name = name
        self.exec_path = exec_path
        self._started = False
        self._delegate = delegate
        self._activated = False

    def __del__(self):
        if self._popen:
            Logger.info('kill subprocess %s' % self._popen.pid)
            self._popen.kill()

    def __str__(self) -> str:
        return 'ASMState `%s` (%s): %s' % (self.name, self.layer_name, self.exec_path)

    def _schedule_response_received(self, _: ScheduleResponseMessage):
        Logger.info('schedule response received')
        self._activated = True

    
    def _yield_received(self, _: YieldMessage):
        Logger.info('yield request received')
        self._activated = False

    def _param_get_handler(self, request: ParamGetRequestMessage):
        if not self._delegate:
            raise RuntimeError('state `%s` delegate not initialized' % self.name)
        Logger.info('gotta request to get param `%s` (%s)' % (request.name, request.typee))

        try:
            value = self._delegate.get_parameter_value(request.name)
        except NoParameterFoundError:
            self._messenger.publish(ParamGetResponseMessage(request=request, status=STATUS_NO_PARAM, value=None))
            raise

        if type(value) != str2typ(request.typee):
            Logger.error('bad parameter type `%s` (got %s, but %s expected)' % (request.name, type(value), request.typee))
            self._messenger.publish(ParamGetResponseMessage(request=request, status=STATUS_BAD_TYPE, value=None))
            return

        self._messenger.publish(ParamGetResponseMessage(request=request, status=STATUS_OK, value=str(value)))
        

    def _param_set_handler(self, request: ParamSetRequestMessage):
        if not self._delegate:
            raise RuntimeError('state `%s` delegate not initialized' % self.name)
        Logger.info('gotta request to set param `%s` (%s) to %s' % (request.name, request.typee, request.value))

        typee = str2typ(request.typee)
        value = typee(request.value)

        try:
            self._delegate.set_parameter_value(request.name, value)
        except NoParameterFoundError:
            self._messenger.publish(ParamSetResponseMessage(request=request, status=STATUS_NO_PARAM))
            raise
        except TypeError:
            self._messenger.publish(ParamSetResponseMessage(request=request, status=STATUS_BAD_TYPE))
            raise
        
        self._messenger.publish(ParamSetResponseMessage(request=request, status=STATUS_OK))
        
    def start(self):
        """
        install asm kernel module
        """
        self._started = True
        self._activated = False

        self._messenger = Messenger(ASM_NAME_PREFIX + self.layer_name, MODULE_NAME_PREFIX + self.name)
        self._messenger.install_callback(ScheduleResponseMessage, self._schedule_response_received)
        self._messenger.install_callback(YieldMessage, self._yield_received)
        self._messenger.install_callback(ParamGetRequestMessage, self._param_get_handler)
        self._messenger.install_callback(ParamSetRequestMessage, self._param_set_handler)

        host, port = EMQ.get_addr()
        self._popen = run_module(self.exec_path, params={
            'emq_host': host,
            'emq_port': port,
            'kernel_name': self.name,
            'layer_name': self.layer_name})

    def schedule(self):
        if not self._started:
            self.start()

        # block until ASMKernel returns or dies
        while not self._activated:
            Logger.info('send message')
            self._messenger.publish(ScheduleRequestMessage())
            sleep()

        Logger.info('activated')
        while self._activated:
            sleep()

        Logger.info('yield!')

    def is_running(self) -> bool:
        return self._activated
