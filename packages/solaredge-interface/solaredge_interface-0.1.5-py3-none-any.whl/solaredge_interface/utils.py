
import requests
from itertools import tee

REQUESTS_TIMEOUT=10


def http_request(url, params=None, timeout=REQUESTS_TIMEOUT):

    if type(params) is dict:
        for item, key in params:
            if type(item) is list:
                params[key] = ','.join(str(item).strip(' '))
            params[key] = str(params[key]).strip(' ')

    r = requests.get(url, params=params, timeout=timeout)
    if r.status_code >= 299:
        r.raise_for_status()

    return r.json()


def url_join(*parts):
    """
    Join terms together with forward slashes

    Parameters
    ----------
    parts

    Returns
    -------
    str
    """
    # first strip extra forward slashes (except http:// and the likes) and
    # create list
    part_list = []
    for part in parts:
        p = str(part)
        if p.endswith('//'):
            p = p[0:-1]
        else:
            p = p.strip('/')
        part_list.append(p)
    # join everything together
    url = '/'.join(part_list)
    return url


def pair_wise(iterable):
    """
    Create pairs to iterate over
    eg. [A, B, C, D] -> ([A, B], [B, C], [C, D])

    Parameters
    ----------
    iterable : iterable

    Returns
    -------
    iterable
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)