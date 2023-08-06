#!/usr/bin/env python3

import os
import sys
import datetime
import threading

import libLemon.Utils.Args as Args

try:
    from colorama import Fore, Back, Style
    _colorful = True
    _log_style_map = {
        'info': Style.DIM,
        'warning': Fore.YELLOW,
        'error': Fore.RED,
        'critical': Back.RED + Fore.WHITE
    }

except:
    _colorful = False
    _log_style_map = dict()

try:
    logging_path = Args.get_arg_str('logging_path')
except:
    if sys.platform == 'win32':
        logging_path = os.path.join(
            os.getcwd(), '__logging__\\%s' % os.path.basename(Args.get_filename()))
    else:
        logging_path = os.path.join(
            os.getcwd(), '__logging__/%s' % os.path.basename(Args.get_filename()))

if not os.path.exists(logging_path):
    os.makedirs(logging_path)

_date_stamp = datetime.datetime.now().strftime(r"%Y_%m_%d")
_fd = open(os.path.join(logging_path, '%s.log' % _date_stamp), 'a')
_fd.write('\n')

_mutex = threading.Lock()

_log_level_map = {
    'info': 0,
    'warning': 10,
    'error': 20,
    'critical': 30
}


_log_level = 'warning'


def set_log_level(level: str):
    global _log_level
    if not level in _log_level_map:
        raise LookupError("unable to find log level %s" % level)
    _log_level = level


def info(msg: str):
    _record(msg, 'info')


def warning(msg: str):
    _record(msg, 'warning')


def error(msg: str):
    _record(msg, 'error')


def critical(msg: str):
    _record(msg, 'critical')


def _record(log: str, typee: str):
    _mutex.acquire()

    try:
        timestamp = datetime.datetime.now().strftime(r"%Y-%m-%d %H:%M:%S.%f")
        log_body = '[%s] [%s] %s' % (timestamp, typee.upper(), log)

        if _log_level_map[typee] >= _log_level_map[_log_level]:
            if _colorful:
                print(_log_style_map[typee], end='')

            print(log_body)

            if _colorful:
                print(Style.RESET_ALL, end='')

        _fd.write(log_body.strip())
        _fd.write('\n')
        _fd.flush()
    except:
        # always release mutex to avoid dead-lock
        _mutex.release()
        raise
    _mutex.release()


if __name__ == '__main__':
    info("this is an info!")
    warning("this is a warning!!")
    error("this is an error!!!")
    critical("this is a critical!!!!")

info('*** Logger initialized for module `%s` ***' % Args.get_filename())
