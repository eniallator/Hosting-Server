import os
import re
import sys
import subprocess
from src.Update import update_project


class Dyno:
    def __init__(self, repo_or_data, branch=None, main=None, project_path=None):
        if branch is None:
            self._load_data(repo_or_data)
        else:
            self._repo = repo_or_data
            self._branch = branch
            self._main = main
            self._project_path = project_path

        self._stdout_logs = b''
        self._stderr_logs = b''
        self._process = None
        self.running = False

    def get_main_path(self):
        return os.path.join(self._project_path, self._main)

    def _load_data(self, data):
        items = [item[1:-1] for item in re.findall(r'"[^"]*"', data)]

        self._repo = items[0]
        self._branch = items[1]
        self._main = items[2]
        self._project_path = items[3]

    def get_data(self):
        return '"' + '", "'.join([self._repo, self._branch, self._main, self._project_path]) + '"'

    def update_project(self, force_update=False):
        update_project(self._project_path, self._repo, self._branch, force=force_update)

    def run(self):
        self.running = True
        self._process = subprocess.Popen(
            (sys.executable, self.get_main_path()),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    def stop(self):
        if self._process is not None:
            self.running = False
            self._process.kill()
            self._process.terminate()

            self._stdout_logs += self._process.stdout.read() + b'\n'
            self._stderr_logs += self._process.stderr.read() + b'\n'

            self._process = None

    def get_logs(self):
        return {'stdout': self._stdout_logs, 'stderr': self._stderr_logs}
