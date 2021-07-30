from typing import Iterable
from multiprocessing import Pool
import os.path
import urllib.parse

from asf_search.exceptions import ASFDownloadError
from asf_search import ASFSession


def _download_url(arg):
    url, path, session = arg
    download_url(
        url=url,
        path=path,
        session=session)


def download_urls(urls: Iterable[str], path: str, session: ASFSession = None, processes: int = 1):
    """
    Downloads all products from the specified URLs to the specified location.

    :param urls: List of URLs from which to download
    :param path: Local path in which to save the product
    :param session: The session to use, in most cases should be authenticated beforehand
    :param processes: Number of download processes to use. Defaults to 1 (i.e. sequential download)
    :return:
    """
    if processes <= 1:
        for url in urls:
            download_url(url=url, path=path, session=session)
    else:
        pool = Pool(processes=processes)
        args = [(url, path, session) for url in urls]
        pool.map(_download_url, args)
        pool.close()
        pool.join()


def download_url(url: str, path: str, filename: str = None, session: ASFSession = None) -> None:
    """
    Downloads a product from the specified URL to the specified location and (optional) filename.

    :param url: URL from which to download
    :param path: Local path in which to save the product
    :param filename: Optional filename to be used, extracted from the URL by default
    :param session: The session to use, in most cases should be authenticated beforehand
    :return:
    """
    if filename is None:
        filename = os.path.split(urllib.parse.urlparse(url).path)[1]

    if not os.path.isdir(path):
        raise ASFDownloadError(f'Error downloading {url}: directory not found: {path}')

    if os.path.isfile(os.path.join(path, filename)):
        raise ASFDownloadError(f'File already exists: {os.path.join(path, filename)}')

    if session is None:
        session = ASFSession()

    print(f'Following {url}')
    response = session.get(url, stream=True, allow_redirects=False)
    print(f'response: {response.status_code}')
    while 300 <= response.status_code <= 399:
        new_url = response.headers['location']
        print(f'Redirect to {new_url}')
        response = session.get(new_url, stream=True, allow_redirects=False)
        print(f'response: {response.status_code}')
    response.raise_for_status()
    with open(os.path.join(path, filename), 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
