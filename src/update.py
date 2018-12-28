import os
from CONFIG import REPO, BRANCH
from requests import get
from json import loads

SHA_FILE = 'SHA_FILE.txt'


def _download(url):
    response = get(url)
    if 200 <= response.status_code < 300:
        return response.content.decode('utf-8')


def get_files_to_download(download_url, to_download={}):
    contents = _download(download_url)

    if contents is None:
        return {}

    repo_content = loads(contents)

    for downloaded_object in repo_content:
        if downloaded_object['type'] == 'file':
            to_download[downloaded_object['name']] = downloaded_object['download_url']
        elif downloaded_object['type'] == 'dir':
            to_download[downloaded_object['name']] = {}
            get_files_to_download(downloaded_object['url'], to_download[downloaded_object['name']])

    return to_download


def replace_files(path, to_download):
    for name, download_url in to_download.items():
        curr_path = os.path.join(path, name)
        if isinstance(download_url, dict):
            nested_files = download_url
            if not os.path.exists(curr_path):
                os.mkdir(path)
            replace_files(curr_path, nested_files)

        else:
            with open(curr_path, 'w') as file_handle:
                contents = _download(download_url)
                if contents is not None:
                    file_handle.write(contents)


def validate_SHA(path):
    page_contents = _download('https://api.github.com/repos/' + REPO + '/commits/' + BRANCH)

    if page_contents is None:
        return True

    content = loads(page_contents)
    last_sha = content['commit']['tree']['sha']
    sha_file_path = os.path.join(path, SHA_FILE)

    if not os.path.isfile(sha_file_path):
        with open(sha_file_path, 'w') as file_handle:
            file_handle.write(last_sha)
        return True

    with open(sha_file_path, 'r') as file_handle:
        if file_handle.read() == last_sha:
            return True

    with open(sha_file_path, 'w') as file_handle:
        file_handle.write(last_sha)
    return False


def update_project(path):
    if validate_SHA(path):
        return

    to_download = get_files_to_download('https://api.github.com/repos/' + REPO + '/contents?ref=' + BRANCH)
    replace_files(path, to_download)

    import app
    app.main()
    raise SystemExit
