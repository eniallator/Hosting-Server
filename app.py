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
        if update_project(project_path, REPO, BRANCH):
            os.system('%s "%s"' % (sys.executable, os.path.join(project_path, 'app.py')))
            raise SystemExit

    dyno_path = os.path.join(project_path, DYNO_FOLDER)
    dyno_manager = DynoManager(dyno_path)
    dyno_manager.add_dyno(name='EniBot', repo='eniallator/Discord-EniBot', branch='master', main='app.py')
    dyno_manager.add_dyno(name='Overwatch', repo='eniallator/Discord-Overwatch-Bot', branch='master', main='app.py')

    dyno_manager._dynos['Overwatch'].update_project()
    dyno_manager.start_dyno('Overwatch')

    import time
    time.sleep(10)

    dyno_manager.stop_dyno('Overwatch')
    print(dyno_manager._dynos['Overwatch'].get_logs())


if __name__ == "__main__":
    main()
