import os

python_exec = r'python3'


def run_module(path: str, params={}):
    os.popen('%s %s %s' % (python_exec, path, ' '.join(
        ['--%s=%s' % (str(k), repr(v)) for k, v in params.items()])))
