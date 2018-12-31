import os
import re
import sys
from src.Dyno import Dyno


DATA_FILE = 'dynos.dat'


class DynoManager:

    def __init__(self, dyno_folder):
        self._dyno_folder = dyno_folder
        self._data_file = os.path.join(dyno_folder, DATA_FILE)

        self._dynos = {}

        if not os.path.exists(self._dyno_folder):
            os.mkdir(self._dyno_folder)
            print('Made dyno folder')
        elif os.path.isfile(self._dyno_folder):
            raise Exception('Dyno folder specified is the path to a file.')

        if not os.path.exists(self._data_file):
            with open(self._data_file, 'w') as file_handle:
                file_handle.write('')
            print('Made data file')
        elif os.path.isdir(self._data_file):
            raise Exception('Dyno data file name exists as a folder')

        self._init_from_data_file()

    def _init_from_data_file(self):
        with open(self._data_file, 'r') as file_handle:
            for data in file_handle.readlines():
                name_match = re.match(r'^[^"]*"(?P<name>[^"]*)":', data)
                name = name_match.group('name')

                dyno_data = re.sub(r'^[^"]*"([^"]*)":', '', data)

                self._dynos[name] = Dyno(dyno_data)

    def _save_data(self, txt):
        with open(self._data_file, 'a') as file_handle:
            prefix = ''
            if os.stat(self._data_file).st_size is not 0:
                prefix = '\n'
            file_handle.write(prefix + txt)

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

        new_dyno = Dyno(repo, branch, main, dyno_path)
        self._dynos[name] = new_dyno

        data = '"' + name + '": ' + new_dyno.get_data()
        self._save_data(data)

        print('Created a new dyno called ' + name)
        return {'success': 'Created dyno'}

    def start_dyno(self, name):
        if name not in self._dynos:
            print('Tried starting a dyno that doesn\'t exist: ' + name)
            return {'error': 'Dyno doesn\'t exist'}
        elif self._dynos[name].running:
            print('Tried starting an already running dyno: ' + name)
            return {'error': 'Dyno already running'}

        dyno = self._dynos[name]
        dyno.run()

        print('Successfully started dyno: ' + name)
        return {'success': 'Started dyno'}

    def stop_dyno(self, name):
        if name not in self._dynos:
            print('Tried stopping a dyno that doesn\'t exist: ' + name)
            return {'error': 'Dyno doesn\'t exist'}
        if not self._dynos[name].running:
            print('Tried stopping a dyno that\'s not running: ' + name)
            return {'error': 'Dyno not running'}

        self._dynos[name].stop()
        print('Successfully stopped dyno: ' + name)
        return {'success': 'Stopped dyno'}
