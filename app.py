from os import path
from src.update import update_project

update_project(path.dirname(path.realpath(__file__)))
