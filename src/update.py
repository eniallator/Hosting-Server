import os
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
        print('Failed to reach: ' + download_url)
        return {}

    repo_content = loads(contents)

    for downloaded_object in repo_content:
        if downloaded_object['type'] == 'file':
            to_download[downloaded_object['name']] = downloaded_object['download_url']
        elif downloaded_object['type'] == 'dir':
            to_download[downloaded_object['name']] = {}
            get_files_to_download(downloaded_object['url'], to_download[downloaded_object['name']])

    return to_download


def replace_files(path, to_download, path_to_print=''):
    for name, download_url in to_download.items():
        curr_path = os.path.join(path, name)
        if isinstance(download_url, dict):
            nested_files = download_url
            if not os.path.exists(curr_path):
                os.mkdir(path)
            replace_files(curr_path, nested_files, path_to_print=os.path.join(path_to_print, name))

        else:
            print('Replacing ' + os.path.join(path_to_print, name))
            with open(curr_path, 'w') as file_handle:
                contents = _download(download_url)
                if contents is not None:
                    file_handle.write(contents)


def validate_SHA(path, repo, branch):
    page_contents = _download('https://api.github.com/repos/' + repo + '/commits/' + branch)

    if page_contents is None:
        print('Failed to get the SHA response from github.')
        return True

    content = loads(page_contents)
    last_sha = content['commit']['tree']['sha']
    sha_file_path = os.path.join(path, SHA_FILE)

    if not os.path.isfile(sha_file_path):
        with open(sha_file_path, 'w') as file_handle:
            file_handle.write(last_sha)
        print('Wrote last SHA.')
        return True

    with open(sha_file_path, 'r') as file_handle:
        if file_handle.read() == last_sha:
            print('Up to date.')
            return True

    with open(sha_file_path, 'w') as file_handle:
        file_handle.write(last_sha)
    print('Wrote new SHA.')
    return False


def update_project(path, repo, branch):
    if validate_SHA(path, repo, branch):
        return

    print('Retrieving files...')
    to_download = get_files_to_download('https://api.github.com/repos/' + repo + '/contents?ref=' + branch)
    replace_files(path, to_download)

    import app
    app.main()
    raise SystemExit
