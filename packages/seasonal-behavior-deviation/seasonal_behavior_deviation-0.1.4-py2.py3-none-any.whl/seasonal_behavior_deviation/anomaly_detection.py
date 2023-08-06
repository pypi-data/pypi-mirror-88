# -*- coding: utf-8 -*-
import logging
import pandas as pd
import numpy as np
from seasonal_behavior_deviation.result import SBDResult
from .util import create_sliding_windows, normalize_column
import math
from fastdtw import fastdtw

__author__ = "Jannik Frauendorf"
__copyright__ = "Jannik Frauendorf"
__license__ = "mit"

_logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# Class containing the logic behind the Seasonal Behavior Deviation algorithm.
# ----------------------------------------------------------------------


class SeasonalBehaviorDeviation(object):
    def __init__(self, data: list, season_length: int, window_size=1, detrend=True, dist_function="euclidean") -> None:
        """
        :param data: list containing the time series with evenly distributed values (i.e., no gaps allowed)
        :param season_length: an integer specifying the number of rows that make up one season
        :param window_size:  This parameter specifies how fine SBD should narrow down the discords.
            With smaller window_size, the anomaly_score vector becomes spikier, and the single anomalies become clear.
            By choosing higher values, the score curve becomes smoother. Moreover, with greater window_sizes, multiple close
            anomalies can be summarized to one larger anomaly.
        :param detrend: flag whether the original data should be de-trended or not

        """

        self.detrend = detrend
        if not isinstance(data, list):
            raise TypeError('Wrong data format. Was expecting a list, got %s.' % type(data))

        self.data = data
        self.season_length = season_length
        self.window_size = window_size
        self.dist_function = dist_function
        self.__result = SBDResult(data)
        self.preprocessed_data = self.__preprocess_data()

    def __preprocess_data(self) -> list:
        # normalize original data
        df = pd.DataFrame({"values": self.data})
        df = normalize_column(df=df, column_name="values")

        return df["values"].tolist()

    def detect(self, data: list = None, season_length: int = None, window_size: int = None,
               detrend: bool = None, dist_function: str = None) -> SBDResult:
        """
        Assigns an anomaly score to each data point of a list by using the Seasonal Behavior Deviation algorithm.
        """

        if data is None:
            data = self.preprocessed_data
        if season_length is None:
            season_length = self.season_length
        if window_size is None:
            window_size = self.window_size
        if detrend is None:
            detrend = self.detrend
        if dist_function is None:
            dist_function = self.dist_function

        series = pd.Series(data)

        if detrend:
            trend_diff, trend = extract_trend(series, season_length)
            detrended_series = detrend_series(series, trend_diff)
            normal_behavior = extract_normal_behavior(detrended_series, season_length)

            # adjust the normal behavior based on the extracted trend
            normal_behavior = adjust_normal_behavior_to_trend(normal_behavior, trend_diff)
        else:
            normal_behavior = extract_normal_behavior(series, season_length)

        scores = compute_anomaly_scores(series, normal_behavior, window_size, dist_function)

        self.__result.set_computed_values(scores=scores.tolist(),
                                          normal_behavior=normal_behavior.tolist(),
                                          normalized_data=series.tolist())

        return self.__result


def adjust_normal_behavior_to_trend(normal_behavior: pd.Series, trend_diff: pd.Series) -> pd.Series:
    # avoid index clashes
    a = normal_behavior.reset_index(drop=True)
    b = trend_diff.reset_index(drop=True)
    return a - b


def extract_trend(series: pd.Series, season_length: int) -> (pd.Series, pd.Series):
    # extract overall trend via moving median
    trend = series.rolling(2 * season_length + 1, center=True).median()

    # the window computation creates NaNs at the beginning and at the end
    # these NaNs are filled with the median of this sequence
    first_window_remainder = series.iloc[[*range(season_length)]].index
    second_window_remainder = series.iloc[[*range(-season_length, 0)]].index
    trend.loc[first_window_remainder,] = series.loc[first_window_remainder].median()
    trend.loc[second_window_remainder,] = series.loc[second_window_remainder].median()

    overall_median = series.median()

    # compute the difference of the values to the trend (moving median) and adjust the values accordingly
    trend_diff = overall_median - trend

    return trend_diff, trend


def detrend_series(series: pd.Series, trend_diff: pd.Series) -> pd.Series:
    detrended_values = series + trend_diff

    return detrended_values


def extract_normal_behavior(series: pd.Series, season_length: int) -> pd.Series:
    """
    Extracts the normal behavior as the median of each season step.
    """
    n = len(series)

    grouped = np.empty((season_length, math.ceil(n / season_length)))
    grouped[:] = np.NaN

    for i, value in enumerate(series):
        i_mod = i % season_length
        i_div = i // season_length
        grouped[i_mod][i_div] = value

    normal_season = []
    for i in range(season_length):
        median = np.nanmedian(grouped[i])
        normal_season.append(median)

    normal_behavior = []
    for i, value in enumerate(series):
        i_mod = i % season_length
        normal_behavior.append(normal_season[i_mod])

    return pd.Series(normal_behavior)


def compute_anomaly_scores(series: pd.Series, normal_behavior: pd.Series, window_size: int,
                           dist_function: str = "euclidean") -> pd.Series:
    # generate sliding window data frame over the normal behavior vector and the value vector (both normalized)
    normal_behavior_windows = create_sliding_windows(normal_behavior, window_size)
    series_behavior_windows = create_sliding_windows(series, window_size)

    # compute scores as row-wise Euclidean Distance between normal behavior and the actual values
    # scores = np.linalg.norm(normal_behavior_windows - series_behavior_windows, axis=1)
    # scores = np.sum(np.abs(normal_behavior_windows - series_behavior_windows), axis = 1)
    scores = compute_distance(normal_behavior_windows, series_behavior_windows, dist_function)

    # move anomaly scores to center of window
    first_part = math.floor((window_size - 1) / 2)
    second_part = math.ceil((window_size - 1) / 2)
    scores = np.concatenate((np.zeros(first_part), scores, np.zeros(second_part)))

    # normalize scores
    df = pd.DataFrame({"scores": scores})
    df = normalize_column(df, "scores")

    return df["scores"]


def compute_distance(a: np.ndarray, b: np.ndarray, dist_function: str = "euclidean") -> np.ndarray:
    if dist_function == "euclidean":
        return np.linalg.norm(a - b, axis=1)
    elif dist_function == "manhattan":
        return np.sum(np.abs(a - b), axis=1)
    elif dist_function == "dtw":
        return np.array([fastdtw(a[i], b[i])[0] for i in range(len(a))])
