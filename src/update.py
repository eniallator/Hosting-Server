import os
from CONFIG import REPO, BRANCH
from requests import get
from json import loads

SHA_FILE = 'SHA_FILE.txt'


def get_files_to_download(download_url, to_download={}):
    response = get(download_url)

    if response.status_code < 200 or response.status_code >= 300:
        return

    repo_content = loads(response.content)

    for dl_file in repo_content:
        if dl_file['type'] == 'file':
            to_download[dl_file['name']] = dl_file['download_url']
        elif dl_file['type'] == 'dir':
            to_download[dl_file['name']] = {}
            get_files_to_download(dl_file['url'], to_download[dl_file['name']])

    return to_download


def update_project(path):
    response = get('https://api.github.com/repos/' + REPO + '/commits/' + BRANCH)

    if response.status_code < 200 or response.status_code >= 300:
        return

    content = loads(response.content)
    last_sha = content['commit']['tree']['sha']
    sha_file_path = os.path.join(path, SHA_FILE)

    if not os.path.isfile(sha_file_path):
        with open(sha_file_path, 'w') as file_handle:
            file_handle.write(last_sha)
        return

    with open(sha_file_path, 'r') as file_handle:
        if file_handle.read() == last_sha:
            return

    to_download = get_files_to_download('https://api.github.com/repos/' + REPO + '/contents?ref=' + BRANCH)
