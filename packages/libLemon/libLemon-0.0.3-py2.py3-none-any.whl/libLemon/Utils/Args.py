#!/usr/bin/env python3

import sys
from pprint import pprint
"""
Currently executing python launching file
"""
_filename = sys.argv[0]

_args = dict()


for argstr in [s.strip() for s in sys.argv[1:]]:
    if argstr.startswith('--'):
        kvstr = argstr[2:]
        if kvstr.count('=') != 1 or kvstr.endswith('='):
            continue
        key, value = kvstr.split('=')
        _args.update({key.strip(): value.strip()})
    elif argstr.startswith('-'):
        if '=' in argstr:
            continue
        _args.update({argstr[1:]: True})
    else:
        pass


def get_filename() -> str:
    return _filename


def get_arg(key: str):
    return _args[key]


def get_arg_str(key: str) -> str:
    return str(_args[key])


def get_arg_int(key: str) -> int:
    return int(_args[key])


def get_arg_float(key: str) -> float:
    return float(_args[key])


def get_arg_bool(key: bool) -> bool:
    value = _args[key]
    if type(value) == str:
        value = value.lower()
    if value in ['yes', 'on', 'true', 'y', 't', '1', 1, True]:
        return True
    elif value in ['no', 'off', 'false', 'n', 'f', '0', 0, 0.0, False, None, 'none', 'null', 'nil', 'undefined', '']:
        return False
    else:
        return True


def override_argument(name: str, value):
    _args.update({name: value})


if __name__ == '__main__':
    pprint(_args)
