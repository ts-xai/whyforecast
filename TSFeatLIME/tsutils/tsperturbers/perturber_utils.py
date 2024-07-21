import numpy as np
import pandas as pd
from typing import Tuple, Union
from tsutils.tsframe import tsFrame


def ts_rolling_mean(
    ts: Union["tsFrame", np.ndarray],
    window_size: int,
):
    """ts_rolling_mean computes rolling mean for tsFrame and numpy ndarray objects.
    The reported rolling mean is of same dimension that of input time series,
    the boundary are adaptively adjusted, for valid window length only.

    Args:
        ts (Union[tsFrame, numpy ndarray]): Time series data, as tsFrame or numpy ndarray object.
        window_size (int): number of consecutive data points over which the averaging
            will be performed.

    Returns:
        df (Union[tsFrame, numpy ndarray]): depending on the input data types the return types is
            set to tsFrame, or numpy ndarray
    """
    df = ts.copy()
    if isinstance(ts, np.ndarray):
        if len(ts.shape) == 1:
            ts = ts.reshape(-1, 1)
        ts = ts.astype("float")
        n_obs, n_vars = ts.shape
        den = np.convolve(
            np.ones(n_obs), np.ones(window_size, dtype="float"), "same"
        ).astype("float")
        df = np.asarray(
            [
                np.convolve(ts[:, i], np.ones(window_size), "same") / den
                for i in range(n_vars)
            ]
        ).T
    elif isinstance(ts, pd.DataFrame):
        dfv = ts_rolling_mean(ts.values, window_size=window_size)
        df.loc[:, ts.columns] = dfv
    return df


def ts_split_mean_residual(
    ts: Union["tsFrame", np.ndarray],
    window_size: int,
):
    ts_avg = ts_rolling_mean(ts, window_size)
    ts_res = ts - ts_avg
    return ts_avg, ts_res
