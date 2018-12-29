import os
import sys
from CONFIG import REPO, BRANCH
from src.Update import update_project

PROD = 'production' in sys.argv


def main():
    if PROD:
        print('Checking for updates...')
        project_path = os.path.dirname(os.path.realpath(__file__))
        update_project(project_path, REPO, BRANCH)


if __name__ == "__main__":
    main()
