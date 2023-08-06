import subprocess

python_exec = r'python3'


def run_module(path: str, params={}) -> subprocess.Popen:
    return subprocess.Popen([python_exec, path] + ['--%s=%s' % (str(k), str(v)) for k, v in params.items()],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE)