import os
from src.update import update_project

try:
    from dev_config import DEV_MODE
except ModuleNotFoundError as err:
    DEV_MODE = False


def main():
    if not DEV_MODE:
        print('Checking for updates...')
        update_project(os.path.dirname(os.path.realpath(__file__)))


if __name__ == "__main__":
    main()
