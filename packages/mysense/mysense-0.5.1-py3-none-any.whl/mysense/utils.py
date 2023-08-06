"""Utilities
"""
import datetime
import decimal
import json
import os
import time

import numpy as np
from dateutil.tz import gettz
from scipy.signal import find_peaks


class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert a DynamoDB item to JSON.
    """

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        elif isinstance(o, np.int64):
            return int(o)
        elif isinstance(o, np.float64):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def now_ts() -> float:
    """
    ts in ms
    """
    return time.time() * 1000


def now_day(days_back: int = 0) -> str:
    """Returns a string with the day of the week in the format:
    Mon, Tue, Wed, Thu, Fri, Sat, Sun
    :param days_back: int (-inf, 0]
    """
    return (datetime.datetime.now(gettz(os.environ['TZ'])) +
            datetime.timedelta(days=days_back)).strftime('%a')


def get_day(ts: float) -> datetime.datetime:
    """
    Datetime object from a ts
    :param ts: timestamp in s or ms
    :return:
    """
    if ts > 5000000000:
        ts /= 1000
    return datetime.datetime.fromtimestamp(ts, tz=gettz(os.environ["TZ"]))


def min_from_midnight(ts: float) -> float:
    """
    Minutes passed since midnight
    :param ts:
    :return:
    """
    return get_day(ts).hour * 60 + get_day(ts).minute


def ms_from_midnight(ts: float) -> float:
    """
    Milliseconds passed since midnight
    :param ts:
    :return:
    """
    if ts > 5000000000:
        ts /= 1000
    today = datetime.datetime.fromtimestamp(ts, tz=gettz(os.environ["TZ"]))
    mid_ts = datetime.datetime(today.year, today.month, today.day,
                               tzinfo=gettz(os.environ['TZ'])).timestamp()
    return (ts - mid_ts) * 1000


def day_of_the_week(ts: float) -> str:
    """
    Returns day of the week for the ts
    :param ts:
    :return:
    """
    return get_day(ts).strftime("%a")


def hour_of_ts(ts: float) -> int:
    """
    Returns the hour of the ts
    :param ts:
    :return:
    """
    return get_day(ts).hour


def hour() -> int:
    """
    Returns the current hour
    """
    return datetime.datetime.now(gettz(os.environ['TZ'])).hour


def minute() -> int:
    """
    Returns the current minute
    """
    return datetime.datetime.now(gettz(os.environ['TZ'])).minute


def tot_min() -> int:
    """
    Minutes from 00:00
    """
    return hour() * 60 + minute()


def midday_ts(days_back: int = 0, ts: float = 0.) -> float:
    """
    The 12:00 local time N days back
    :param ts:
    :param days_back:
    :return: ts in ms
    """
    if ts > 5000000000:
        ts /= 1000
    if not ts:
        today = datetime.datetime.now(gettz(os.environ['TZ']))
        yesterday = datetime.datetime(today.year, today.month, today.day, 12,
                                      tzinfo=gettz(os.environ['TZ'])) - \
                    datetime.timedelta(days=days_back)
        return yesterday.timestamp() * 1000
    else:
        day = datetime.datetime.fromtimestamp(ts, tz=gettz(os.environ["TZ"]))
        return datetime.datetime(day.year,
                                 day.month,
                                 day.day,
                                 12,
                                 tzinfo=gettz(os.environ['TZ'])).timestamp() * 1000


def midday_datetime_from_date(date: datetime.datetime) -> datetime.datetime:
    """
    Convert date to datetime with time being midday
    :param date: datetime.date object
    :return: datetime.datetime object
    """
    date_time = datetime.datetime.combine(date,
                                          datetime.time(12, 0),
                                          tzinfo=gettz(os.environ["TZ"]))
    return date_time


def midnight_ts(days_back: int = 0) -> float:
    """
    The 00:00 local time N days back
    :param days_back:
    :return: ts in ms
    """
    today = datetime.datetime.now(gettz(os.environ['TZ']))
    yesterday = datetime.datetime(today.year, today.month, today.day, 0,
                                  tzinfo=gettz(os.environ['TZ'])) - \
                datetime.timedelta(days=days_back)
    return yesterday.timestamp() * 1000


def day_hour_ts(days_back: int = 0, hour: int = 0) -> float:
    """
    The 'hh' local time N days back
    :param days_back: how many days back (-inf, 0]
    :param hour: the hour of the day [0, 23]
    :return: ts in ms
    """
    today = datetime.datetime.now(gettz(os.environ['TZ']))
    yesterday = datetime.datetime(today.year, today.month, today.day, hour,
                                  tzinfo=gettz(os.environ['TZ'])) + \
                datetime.timedelta(days=days_back)
    return yesterday.timestamp() * 1000


def hours_back(hours_to_subtract: int = 0) -> float:
    """[summary]

    :param hours_to_subtract: [description], defaults to 0
    :type hours_to_subtract: int, optional
    :return: [description]
    :rtype: float
    """
    today = datetime.datetime.now(gettz(os.environ["TZ"]))
    yesterday = datetime.datetime(today.year, today.month, today.day, today.hour,
                                  tzinfo=gettz(os.environ["TZ"])) - \
                datetime.timedelta(hours=hours_to_subtract)
    return yesterday.timestamp() * 1e3


def benchmark(display_func):
    """
    Used to time functions
    :param display_func: function to display the results, e.g. print
    :return:
    """

    def time_it(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            res = func(*args, **kwargs)
            display_func(f"{func.__name__} executed in {time.perf_counter() - start:.3f}s")
            return res

        return wrapper

    return time_it


def age(dob: str) -> int:
    """
    This function converts the dob to age for a user.
    :param dob: date of birth should be of the format d-m-y
    :return: age
    """
    try:
        dob = datetime.datetime.strptime(dob, '%d-%m-%Y')
    except ValueError:
        return -1
    today = datetime.datetime.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def ewma(y: float, y_0: float, std: float, span: int = 7) -> tuple:
    """
    Exponentialy weighted moving average
    :param y: new stat record
    :param y_0: current average value of a statistic
    :param std: current standard deviation of a statistic
    :param span: decay parameter
    :return: new average and std
    """
    alpha = 2 / (span + 1)
    y_ = y_0
    var = std ** 2
    delta = y - y_
    var = (1 - alpha) * (var + alpha * delta ** 2)
    y_ += alpha * delta

    return y_, np.sqrt(var)


def stats_update(count: int, mean: float, std: float, new_value: float):
    """
    Online update of the statistics
    :param count: total number of points in the statistic
    :param mean: current mean
    :param std: current standard deviation
    :param new_value: new value of the statistic
    :return: new count, mean and standard deviation
    """
    var = std ** 2
    M2 = var * count
    count += 1
    delta = new_value - mean
    mean += delta / count
    delta2 = new_value - mean
    M2 += delta * delta2
    return count, mean, np.sqrt(M2 / count)


def check_dict_structure(dict_template: dict, dict_to_check: dict) -> dict:
    """
    Checks if all required fields are present, if not – initialises them
    :param dict_to_check:
    :param dict_template:
    :return:
    """

    def update_structure(dict1: dict, dict2: dict):
        for item in set(dict1) - set(dict2):
            dict2.update({item: dict1[item]})
        for item in set(dict2) - set(dict1) - {"cid"}:
            dict2.pop(item)

    def check_structure(dict1: dict, dict2: dict):
        for item in set(dict1) & set(dict2):
            if isinstance(dict1[item], dict) and isinstance(dict2[item], dict):
                check_structure(dict1[item], dict2[item])
            elif (isinstance(dict1[item], dict)
                  or (isinstance(dict2[item], (float, int)) and (isinstance(dict1[item], list)))
                  or (isinstance(dict1[item], (float, int)) and (isinstance(dict2[item], list)))):
                dict2.update({item: dict1[item]})
        update_structure(dict1, dict2)

    check_structure(dict_template, dict_to_check)

    return dict_to_check


def batcher(seq, batch_size: int) -> list:
    """Splits an iterable into batch sized iterables

    :param seq: iterable to split into batches
    :type seq: list, tuple, set
    :param batch_size: batch size
    :type batch_size: int
    :return: yields a list with 'batch_size' items
    :rtype: list
    """
    res = []
    for el in seq:
        res.append(el)
        if len(res) == batch_size:
            yield res
            res = []
    if res:
        yield res


def activity_density(ts_list, ts_grid, sigma) -> np.array:
    """
    Calculates the activity density function
    :param ts_list: The list of timestamps for a particular sensor or a group of sensors
    :param ts_grid: timestamp grid
    :param sigma: sigma/width of the gaussian function used to calculate the density
    :return: activity density function
    """
    ts_matrix = ts_grid[:, np.newaxis] - ts_list
    dens = np.exp(-ts_matrix ** 2 / 2 / sigma ** 2).sum(axis=1)
    return dens


def activity_filter(ts_grid: np.array, activ_dens: np.array) -> np.array:
    """
    This function finds the peaks of activity, and return a list of corresponding
    timestamps. Activity density function and timestamp grid should have the same length.
    Should be applied to activity density function from a 'noisy' sensor, such as vibration sensor,
    or door sensor.
    :param ts_grid: timestamp grid
    :param activ_dens: activity density function
    :return: An np.array of timestamps
    """
    peak_indices, _ = find_peaks(activ_dens)
    return ts_grid[peak_indices]


def convert_to_float(structure: dict) -> dict:
    """
    Convert all Decimal numbers to float
    :param structure:
    :return:
    """
    return json.loads(json.dumps(structure, cls=DecimalEncoder))


def convert_to_decimal(structure: dict) -> dict:
    """
    Convert all float and int numbers to Decimal for DynamoDB compatibility
    :param structure:
    :return:
    """
    return json.loads(json.dumps(convert_to_float(structure)),
                      parse_float=decimal.Decimal,
                      parse_int=decimal.Decimal)

