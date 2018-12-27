import os
from CONFIG import REPO, BRANCH
from requests import get
from json import loads

SHA_FILE = 'SHA_FILE.txt'


def update():
    pass


def update_project(path):
    response = get('https://api.github.com/repos/' + REPO + '/commits/' + BRANCH)
    content = loads(response.content)
    last_sha = content['commit']['tree']['sha']
    sha_file_path = os.path.join(path, SHA_FILE)

    if not os.path.isfile(sha_file_path):
        with open(sha_file_path, 'w') as file_handle:
            file_handle.write(last_sha)
        return

    with open(sha_file_path, 'r') as file_handle:
        if file_handle.read() != last_sha:
            update()
