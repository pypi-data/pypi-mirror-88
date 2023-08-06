#!/usr/bin/env python3


from typing import Any
from libLemon.ASM.Message.ParamSetRequestMessage import ParamSetRequestMessage
from libLemon.Utils.Utilities import str2typ, typ2str

from abc import ABC, abstractmethod

import libLemon.Utils.Args as Args
import libLemon.Utils.Logger as Logger
from libLemon.MTP import EMQ
from libLemon.ASM.Entity import ASMParameter
from libLemon.MTP.Messenger import Messenger
from libLemon.ASM.Message import ParamGetRequestMessage, ScheduleRequestMessage, ScheduleResponseMessage, YieldMessage, ParamGetResponseMessage, ParamSetResponseMessage
from libLemon.Utils.Const import ASM_NAME_PREFIX, MODULE_NAME_PREFIX, STATUS_OK, STATUS_ERR
from libLemon.Utils.Sleep import sleep

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
        Logger.info('host, port = %s, %d' % (self.host, self.port))

    @abstractmethod
    def kernel_init(self):
        pass

    @abstractmethod
    def kernel_workload(self):
        pass

    def _kernel_awake(self):
        while not self._activated:
            sleep()
        self._messenger.publish(ScheduleResponseMessage(status=STATUS_OK,request=self._schedule_request))
        self._schedule_request = None

    def _kernel_yield(self):
        self._activated = False
        self._messenger.publish(YieldMessage())

    def _schedule_request_received(self, payload: ScheduleRequestMessage):
        Logger.info('schedule request received')
        self._schedule_request = payload
        self._activated = True



    def start(self):
        self._activated = False
        self._messenger = Messenger(MODULE_NAME_PREFIX + self.name, ASM_NAME_PREFIX + self.layer_name)
        self._messenger.install_callback(ScheduleRequestMessage, self._schedule_request_received)

        self._param_get_callback_queue = dict()
        self._param_get_value_queue = dict()
        self._messenger.install_callback(ParamGetResponseMessage, callback=self._param_get_received)

        self._param_set_callback_queue = dict()
        self._param_set_value_queue = dict()
        self._messenger.install_callback(ParamSetResponseMessage, callback=self._param_set_received)

        self.kernel_init()
        while True:
            self._kernel_awake()
            self.kernel_workload()
            self._kernel_yield()

    # async call's callback function here
    _param_get_callback_queue: dict[ParamGetRequestMessage: Any]
    _param_set_callback_queue: dict[ParamSetRequestMessage: Any]

    # sync call's data cache
    _param_get_value_queue: dict[ParamGetRequestMessage: tuple]
    _param_set_value_queue: dict[ParamSetRequestMessage: bool]

    def _param_get_received(self, payload: ParamGetResponseMessage):
        Logger.info(str(payload))
        request = payload.request
        Logger.info(str(request))
        typee = str2typ(request.typee)
        state, value = payload.status, typee(payload.value)
        if request in self._param_get_callback_queue:
            Logger.info('async style!!')
            self._param_get_callback_queue[request]((state, value))
        else:
            Logger.info('sync style!!')
            self._param_get_value_queue[request] = (state, value)

    def _param_set_received(self, payload: ParamSetResponseMessage):
        request = payload.request
        state = payload.status
        if request in self._param_set_callback_queue:
            self._param_set_callback_queue[request](state)
        else:
            self._param_set_value_queue[request] = state

    def get_parameter(self, param: ASMParameter) -> object:
        msg = ParamGetRequestMessage(name=param.name, typee=typ2str(param.typee))
        self._param_get_value_queue.update({msg: None})
        self._messenger.publish(msg)
        while self._param_get_value_queue[msg] == None:
            sleep()

        state, value = self._param_get_value_queue[msg]
        if state != STATUS_OK:
            raise RuntimeError('parameter get request returned error state %s' % state)
            
        del self._param_get_value_queue[msg]
        return value
    
    def set_parameter(self, param: ASMParameter):
        msg = ParamSetRequestMessage(name=param.name, typee=typ2str(param.typee), value=str(param.value))
        self._param_set_value_queue.update({msg: None})
        self._messenger.publish(msg)
        while self._param_set_value_queue[msg] == None:
            sleep()
        
        state = self._param_set_value_queue[msg]
        if state != STATUS_OK:
            raise RuntimeError('parameter set request returned error state %s' % state)

        del self._param_set_value_queue[msg]

    def get_parameter_async(self, param: ASMParameter, callback):
        msg = ParamGetRequestMessage(name=param.name, typee=typ2str(param.typee))
        self._param_get_callback_queue.update({msg: callback})
        self._messenger.publish(msg)
    
    def set_parameter_async(self, param: ASMParameter, callback):
        msg = ParamSetRequestMessage(name=param.name, typee=typ2str(param.type), value=str(param.value))
        self._param_set_callback_queue.update({msg: callback})
        self._messenger.publish(msg)