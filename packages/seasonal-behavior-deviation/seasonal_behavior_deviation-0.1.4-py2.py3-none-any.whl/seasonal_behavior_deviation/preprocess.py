import logging
import pandas as pd

__author__ = "Jannik Frauendorf"
__copyright__ = "Jannik Frauendorf"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def preprocess(data, season_length):
    """
    Convenience function to orchestrate other preprocessing functions.

    :param data: pandas Series containing the given time series.
    :param season_length: an integer specifying the number of rows that make up one season
    :return: tuple with
                - processed pandas DataFrame
                - the name of the column containing the time series data
                - the name of the original index
    """

    df, value_column_name, previous_index_name = build_df(data=data)
    df = add_season_steps(df=df, season_length=season_length)
    return df, value_column_name, previous_index_name


def build_df(data):
    """
    Creates and returns a pandas DataFrame from the given pandas Series with the original index as a column.
    It also extracts and returns the original column and index name to restore the DataFrame to its original column
    and index name.

    :param data: pandas Series
    :return: tuple with
                - processed pandas DataFrame
                - the name of the column containing the time series data
                - the name of the original index
    """

    # retrieve original column and index name
    value_column_name = data.name
    previous_index_name = data.index.name

    if previous_index_name is None:
        previous_index_name = "index"

    df = pd.DataFrame(data)

    # set index to running number
    df = df.reset_index()

    return df, value_column_name, previous_index_name


def add_season_steps(df, season_length):
    """
    Adds a column to the DataFrame containing the season step depending on the given season_length.
    The season step determines the position of each column within a season. It ranges from 0 to season_length - 1.

    :param df: pandas DataFrame with a DateTime index and a column containing the time series values.
    :param season_length: an integer specifying the number of rows that make up one season
    :return: pandas DataFrame
    """
    df.loc[:, 'season_step'] = df.index % season_length
    return df
