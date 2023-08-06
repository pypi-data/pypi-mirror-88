from time import sleep as _sleep

_sleep_span = 0.1

def sleep(seconds: float = _sleep_span):
    _sleep(seconds)