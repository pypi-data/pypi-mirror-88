# (c) 2012-2018 Dativa, all rights reserved
# -----------------------------------------
#  This code is licensed under MIT license (see license.txt for details)

"""
A set of functions to improve dataframe column handling in pandas
"""

import numpy as np
import pandas as pd
from pandas._libs.tslibs.strptime import array_strptime
from pandas._libs import tslib
from pandas.core.dtypes.generic import ABCIndexClass, ABCSeries
from pandas.core.dtypes.common import is_list_like
from pandas import Series, DatetimeIndex
from datetime import datetime


def is_numeric(series_or_string):
    """
    Returns whether the series or string isnumeric
    """
    if not pd:  # pragma: no cover
        raise ImportError("pandas must be installed to run is_numeric")

    if isinstance(series_or_string, pd.Series):
        return np.isreal(series_or_string).all()
    else:
        try:
            float(series_or_string)
            return True
        except ValueError:
            return False


def get_column_name(df, column, total_columns=None):
    """
    gets the name of a column from either an integer or a passed name.
    Allows the total columns to be overwritten for cases where additional columns
    are added to the dataframe.
    """
    if total_columns is None:
        total_columns = df.shape[1]

    if column in df.columns:
        return column

    try:
        column_index = int(column)
        if column_index < 0:
            column_index = column_index + total_columns
        return df.columns.values.tolist()[column_index]
    except (ValueError, TypeError):  # we should be testing this?
        raise KeyError('Invalid column name: {0} not in {1}'.format(column, df.columns))


def get_unique_column_name(df, name, suffix='_clean'):
    """
    Gets a unique name for a new column
    """

    if name not in df.columns:
        return name
    else:
        return get_unique_column_name(df, str(name) + suffix)


def string_to_datetime(series_or_string, format, errors="raise"):
    """
    Converts a series (or string) to a timestamp according
    to the passed format string.
    """
    pd_old_version = "0.23.4"

    if format == "%s":
        # Please remove the no cover this as soon as possible and add tests to cover this
        if errors == "raise" and not is_numeric(series_or_string):  # pragma: no cover
            raise ValueError()
        else:
            return pd.to_datetime(series_or_string, unit='s', errors=errors)
    else:
        # hard coded subset of pd.to_datetime to prevent automatic recognition of ISO8601 format
        # Please remove the no cover this as soon as possible and add tests to cover this
        if isinstance(series_or_string, tslib.Timestamp): # pragma: no cover
            return DatetimeIndex(series_or_string)
        elif isinstance(series_or_string, ABCSeries):
            values = array_strptime(series_or_string._values, format, exact=True, errors=errors)
            if pd.__version__ > pd_old_version:
                values = values[0]
            return Series(DatetimeIndex(values), index=series_or_string.index, name=series_or_string.name)
        # Please remove the no cover this as soon as possible and add tests to cover this
        elif isinstance(series_or_string, ABCIndexClass):  # pragma: no cover
            values = array_strptime(series_or_string._values, format, exact=True, errors=errors)
            if pd.__version__ > pd_old_version:
                values = values[0]
            return DatetimeIndex(values)
        # Please remove the no cover this as soon as possible and add tests to cover this
        elif is_list_like(series_or_string):  # pragma: no cover
            values = array_strptime(series_or_string._values, format, exact=True, errors=errors)
            if pd.__version__ > pd_old_version:
                values = values[0]
            return DatetimeIndex(values)
        else:
            values = array_strptime(pd.Series([series_or_string]).values, format, exact=True, errors=errors)
            if pd.__version__ > pd_old_version:
                values = values[0]
            return DatetimeIndex(values)[0]


def _datetime_to_string(timestamp, format):
    try:
        if format == "%s":
            return "{0:.0f}".format((timestamp - datetime(1970, 1, 1)).total_seconds())
        else:
            return timestamp.strftime(format)
    except ValueError:
        return None


def datetime_to_string(timestamp, format):
    """
    Takes an individual timestamp and returns a string according to
    the passed format
    """
    if not pd:  # pragma: no cover
        raise ImportError("pandas must be installed to run datetime_to_string")

    if type(timestamp) is pd.Series:
        return timestamp.apply(lambda x: _datetime_to_string(x, format))
    else:
        return _datetime_to_string(timestamp, format)


def format_string_is_valid(format):
    """
    Checks a format string to see whether it returns anything date like
    """
    if not pd:  # pragma: no cover
        raise ImportError("pandas must be installed to run format_string_is_valid")

    date1 = datetime(1, 2, 3, 4, 5, 6, 7)
    date2 = datetime(8, 9, 10, 11, 12, 13, 14)
    if _datetime_to_string(date1, format) == _datetime_to_string(date2, format):
        return False

    return True
