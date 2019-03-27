import atexit
import subprocess
import time

from .helper.path import REPO_ROOT


# Should we use weakref?  I think this is sufficient in this case.
_SIMULATORS = []


def _python_exit():
    for s in _SIMULATORS:
        s.kill()


atexit.register(_python_exit)


class Simulator:
    SCRIPT_PATH = REPO_ROOT / 'script/launch_simulator.sh'

    def __init__(self, port):
        self._port = port
        self._proc = None

        _SIMULATORS.append(self)

    def connect(self):
        assert self._proc is None

        # options = ['-n 1 --limithp 100']
        options = ['-n', '1']
        # options = []
        command = [self.SCRIPT_PATH.as_posix()] + options
        self._proc = subprocess.Popen(command, start_new_session=True, stdout=subprocess.DEVNULL)
        time.sleep(5)

    def kill(self):
        if self._proc:
            self._proc.kill()
            self._proc.wait()
            self._proc = None

    def __del__(self):
        self.kill()
