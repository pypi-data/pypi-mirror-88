#!/usr/bin/env python3

from libLemon.Error.Error import EMQInitError
import libLemon.Utils.Args as Args

_host: str = None
_port: int = None

def set_addr(host: str, port: int):
    global _host, _port
    assert(0 <= port <= 65535)
    _host, _port = host, port

def get_addr() -> tuple[str, int]:
    global _host, _port
    if _host == None:
        try:
            _host = Args.get_arg_str('emq_host')
        except KeyError:
            raise EMQInitError('no emq_host provided when initializing emq')
    if _port == None:
        try:
            _port = Args.get_arg_int('emq_port')
        except KeyError:
            raise EMQInitError('no emq_port provided when initializing emq')
    
    assert(0 <= _port <= 65535)
    return (_host, _port)