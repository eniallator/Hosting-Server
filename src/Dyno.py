class Dyno:
    def __init__(self, repo, branch, main_script, project_path):
        self._repo = repo
        self._branch = branch
        self._main_script = main_script
        self._project_path = project_path
