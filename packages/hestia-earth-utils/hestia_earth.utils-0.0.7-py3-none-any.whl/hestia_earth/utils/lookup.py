from functools import reduce
import csv
import numpy

DELIMITER = '\t'
ENCODING = 'ISO-8859-1'


def _recfromcsv_mod(filename: str, **kwargs):
    def rewrite_csv_as_tab():
        with open(filename, 'r', encoding=ENCODING) as fp:
            reader = csv.reader(fp)
            for row in reader:
                yield DELIMITER.join(row)
    return numpy.recfromcsv(rewrite_csv_as_tab(), delimiter=DELIMITER, **kwargs)


def load_lookup(filename: str):
    """
    Import lookup table as csv file into a `numpy.recarray`.

    Parameters
    ----------
    filename : str
        The name of the file.

    Returns
    -------
    numpy.recarray
        The `numpy.recarray` converted from the csv content.
    """
    return _recfromcsv_mod(filename, encoding=ENCODING)


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
        print(values)
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
