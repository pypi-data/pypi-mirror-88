#!/usr/bin/env python3

import libLemon.Utils.Args as Args

_host: str = None
_port: int = None

def get_addr() -> tuple[str, int]:
    global _host, _port
    if _host == None:
        _host = Args.get_arg_str('emq_host')
    if _port == None:
        _port = Args.get_arg_int('emq_port')
    
    assert(0 <= _port <= 65535)
    return (_host, _port)