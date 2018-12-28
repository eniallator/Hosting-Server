from os import path
from src.update import update_project


def main():
    update_project(path.dirname(path.realpath(__file__)))


if __name__ == "__main__":
    main()
