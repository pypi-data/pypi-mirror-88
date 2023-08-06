from functools import reduce
import os
from io import StringIO
import requests
import csv
import numpy

from .s3_client import _load_from_bucket
from .request import request_url, web_url

DELIMITER = '\t'
ENCODING = 'ISO-8859-1'


def _rewrite_csv_file_as_tab(filepath: str):
    with open(filepath, 'r', encoding=ENCODING) as fp:
        reader = csv.reader(fp)
        for row in reader:
            yield DELIMITER.join(row)


def _rewrite_csv_text_as_tab(text: str):
    reader = csv.reader(StringIO(text))
    for row in reader:
        yield DELIMITER.join(row)


def _recfromcsv(data, **kwargs): return numpy.recfromcsv(data, delimiter=DELIMITER, **kwargs)


def load_lookup(filepath: str):
    """
    Import local lookup table as csv file into a `numpy.recarray`.

    Parameters
    ----------
    filepath : str
        The path of csv file on the local file system.

    Returns
    -------
    numpy.recarray
        The `numpy.recarray` converted from the csv content.
    """
    return _recfromcsv(_rewrite_csv_file_as_tab(filepath), encoding=ENCODING)


def _download_lookup_data(filename: str):
    try:
        return _load_from_bucket(os.getenv('AWS_BUCKET_GLOSSARY'), f"lookups/{filename}")
    except ImportError:
        url = request_url(f"{web_url()}/glossary/lookups/{filename}")
        return requests.get(url).content.decode('utf-8')


def download_lookup(filename: str):
    """
    Download lookup table from Hestia as csv into a `numpy.recarray`.

    Parameters
    ----------
    filename : str
        The name on the file on the Hestia lookup repository.

    Returns
    -------
    numpy.recarray
        The `numpy.recarray` converted from the csv content.
    """
    try:
        return _recfromcsv(_rewrite_csv_text_as_tab(_download_lookup_data(filename)), encoding=ENCODING)
    except ValueError:
        return None


def column_name(key: str):
    """
    Convert the column name to a usable key on a `numpy.recarray`.

    Parameters
    ----------
    key : str
        The column name.

    Returns
    -------
    str
        The column name that can be used in `get_table_value`.
    """
    return key.replace(',', '').replace(' ', '_').lower()


def _get_single_table_value(array: numpy.recarray, col_match, col_match_with, col_val):
    return array[array[col_match] == col_match_with][col_val][0]


def get_table_value(array: numpy.recarray, col_match, col_match_with, col_val):
    """
    Get a value matched by one or more columns from a `numpy.recarray`.

    Parameters
    ----------
    array : numpy.recarray
        The array returned by the `load_lookup` function.
    col_match
        Which `column` should be used to find data in. This will restrict the rows to search for.
        Can be a single `str` or a list of `str`. If a list is used, must be the same length as `col_match_with`.
    col_match_with
        Which column `value` should be used to find data in. This will restrict the rows to search for.
        Can be a single `str` or a list of `str`. If a list is used, must be the same length as `col_match`.
    col_val: str
        The column which contains the value to look for.

    Returns
    -------
    str
        The value found or `None` if no match.
    """
    def reducer(x, values):
        col = values[1]
        value = col_match_with[values[0]]
        return x[x[col] == value]

    single = isinstance(col_match, str) and isinstance(col_match_with, str)
    try:
        return _get_single_table_value(array, col_match, col_match_with, col_val) if single else \
            reduce(reducer, enumerate(col_match), array)[col_val][0]
    except IndexError:
        return None
    except ValueError:
        return None
