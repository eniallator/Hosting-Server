import os
import sys
from src.update import update_project

PROD = 'production' in sys.argv


def main():
    if PROD:
        print('Checking for updates...')
        update_project(os.path.dirname(os.path.realpath(__file__)))


if __name__ == "__main__":
    main()
