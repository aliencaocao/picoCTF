import json
import hashlib
import requests

API_URL = 'https://libc.rip/api/find'


def search(known_symbols: dict[str, str]) -> dict[str, str]:
    """
    Search for the libc version using the known symbols and their offsets.
    :param: known_symbols: A dictionary of known symbols and their offsets in the format {'symbol': 'offset'}.

    :returns: The libc information found.
    """
    assert isinstance(known_symbols, dict), 'known_symbols must be a dictionary!'
    assert len(known_symbols) >= 2, 'known_symbols must be at least 2 pairs!'
    r = requests.post(API_URL, json={'symbols': known_symbols})
    if r.status_code == 200:
        r = json.loads(r.text)
        if not len(r):
            raise Exception('No results found!')
        elif len(r) == 1:
            return r[0]
        else:
            raise Exception('Multiple libc versions found! Please supply more symbols.')
    else:
        raise Exception(f'Search failed. Response code: {r.status_code}. Error: {r.text}')


def download(url: str, path: str, hash: str = None) -> str:
    r = requests.get(url)
    if r.status_code == 200:
        if hash:
            if hashlib.sha256(r.content).hexdigest() != hash:
                raise Exception('Downloaded file does not match the hash!')
        with open(path, 'wb') as f:
            f.write(r.content)
        return path
    else:
        raise Exception(f'Download failed. Response code: {r.status_code}. Error: {r.text}')


def search_and_download(known_symbols: dict[str, str]) -> str:
    """
    Search for the libc version using the known symbols and their offsets, then download the libc into the current working directory.
    :param: known_symbols: A dictionary of known symbols and their offsets in the format {'symbol': 'offset'}.

    :returns: The path to the downloaded libc file.
    """
    result = search(known_symbols)
    print(f'Found libc: {result["id"]}, downloading now from {result["download_url"]}')
    path = result['download_url'].split('/')[-1]
    path = download(result['download_url'], path, result['sha256'])
    print(f'Downloaded libc to {path}')
    return path

# search_and_download({'fgets': '0x7fe7f9d08660', 'puts': '0x7fe7f9d0a450'})
