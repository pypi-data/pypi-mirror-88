import os


def api_url(): return os.environ.get('API_URL', 'https://api.hestia.earth')


def search_url(): return os.environ.get('SEARCH_URL', 'https://search.hestia.earth')


def web_url(): return os.environ.get('WEB_URL', 'https://hestia.earth')


def non_empty_value(value):
    """
    Return True if the value is not en empty string or an empty list.

    Parameters
    ----------
    value
        Either a string, a list, a number or None.
    """
    return value != '' and value is not None and value != []


def join_args(values): return '&'.join(list(filter(non_empty_value, values))).strip()


def request_url(base_url: str, **kwargs):
    args = list(map(lambda key: '='.join([key, str(kwargs.get(key))]) if kwargs.get(key) else None, kwargs.keys()))
    return '?'.join(list(filter(non_empty_value, [base_url, join_args(args)]))).strip()
