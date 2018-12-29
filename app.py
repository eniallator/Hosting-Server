import os
import sys
from CONFIG import REPO, BRANCH, DYNO_FOLDER
from src.Update import update_project
from src.DynoManager import DynoManager

PROD = 'production' in sys.argv


def main():
    project_path = os.path.dirname(os.path.realpath(__file__))

    if PROD:
        print('Checking for updates...')
        update_project(project_path, REPO, BRANCH)

    dyno_path = os.path.join(project_path, DYNO_FOLDER)
    dyno_manager = DynoManager(dyno_path)
    dyno_manager.add_dyno(name='foo_bar', repo='eniallator/Discord-Overwatch-Bot', branch='master', main='app.py')


if __name__ == "__main__":
    main()
