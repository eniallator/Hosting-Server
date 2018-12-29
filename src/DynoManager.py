import os
import threading
from src.Dyno import Dyno


class DynoManager:

    def __init__(self, dyno_folder):
        self._dynos = {}
        self._dyno_folder = dyno_folder

        if not os.path.exists(dyno_folder):
            print("Made dyno folder")
            os.mkdir(dyno_folder)
        elif os.path.isfile(dyno_folder):
            raise Exception('Dyno folder specified is the path to a file.')

    def add_dyno(self, name, repo, branch, main):
        dyno_path = os.path.join(self._dyno_folder, name)

        if os.path.exists(dyno_path):
            print('Dyno already exists: ' + name)
            return {'error': 'Dyno already exists'}

        try:
            os.mkdir(dyno_path)
        except OSError:
            print('Invalid name for dyno: ' + name)
            return {'error': 'Dyno name invalid'}

        self._dynos[name] = Dyno(repo, branch, main, dyno_path)
        print('Created a new dyno called ' + name)
        return {'succes': 'Created dyno'}
