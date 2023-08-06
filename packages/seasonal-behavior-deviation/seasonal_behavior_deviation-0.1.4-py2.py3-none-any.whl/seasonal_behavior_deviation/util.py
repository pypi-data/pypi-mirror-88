# -*- coding: utf-8 -*-
import logging
from skimage.util.shape import view_as_windows
import numpy as np
import pandas as pd

__author__ = "Jannik Frauendorf"
__copyright__ = "Jannik Frauendorf"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def create_sliding_windows(series, window_size):
    """
    Computes the result of a sliding window over the given vector with the given window size.
    Each row represents the content of the sliding window at each position.

    :param series: pandas Series containing the time series
    :param window_size: an integer specifying the width of the sliding window.
    :return: pandas DataFrame
    """
    vector = np.array(series)
    return pd.DataFrame(view_as_windows(vector, window_size))


def normalize_column(df, column_name, new_column_name=None):
    """
    Normalize the given column in the given DatFrame linearly between 0 and 1.
    If no new_column_name is given the original data will be replaced.

    :param df: a pandas data frame that contains at least the given column_name
    :param column_name: a string that specifies the column name that should be normalized
    :param new_column_name: a string that specifies the column name of the normalized values
    :return: pandas DataFrame
    """

    if new_column_name is None:
        new_column_name = column_name

    column_min = df[column_name].min()
    column_max = df[column_name].max()

    # linear normalization
    df.loc[:, new_column_name] = (df[column_name] - column_min) / (column_max - column_min)
    return df

