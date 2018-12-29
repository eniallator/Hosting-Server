import re
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

    def _load_data(self, data):
        items = re.findall(r'"[^"]*"', data)

        self._repo = items[0]
        self._branch = items[1]
        self._main = items[2]
        self._project_path = items[3]

    def get_data(self):
        return '"' + '", "'.join([self._repo, self._branch, self._main, self._project_path]) + '"'

    def update_project(self, force_update):
        update_project(self._project_path, self._repo, self._branch, force=force_update)
