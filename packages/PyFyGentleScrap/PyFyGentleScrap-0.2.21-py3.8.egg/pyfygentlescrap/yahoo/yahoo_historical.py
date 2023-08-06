# coding: utf-8
# !/usr/bin/python3

import json
import logging
import pandas
import pyfygentlescrap as pfgs
import requests
import urllib

from json.decoder import JSONDecodeError
from pyfygentlescrap.yahoo.yahoo_shared import _timestamp_to_datetime
from pyfygentlescrap.yahoo.yahoo_shared import _to_utc_timestamp
from requests.exceptions import ConnectTimeout
from requests.exceptions import ConnectionError

logger = logging.getLogger(__name__)


def _empty_dataframe():
    """ Returns an empty dataFrame with columns name."""
    cols = ["open", "high", "low", "close", "adjclose", "volume", "dividend", "split"]
    return pandas.DataFrame(columns=cols)


def _parse_query_to_pandas(http_response_text):
    """
    Go through ``json`` pre-parsed requests to convert all the data
    into a ``pandas.DataFrame``.

    Args:
        http_response_text: a valid requests http response

    Returns:
        DataFrame
    """

    # Convert the parameter to json:
    try:
        _json = json.loads(http_response_text)
    except JSONDecodeError:
        return _empty_dataframe()

    _json = _json["chart"]["result"][0]
    # Creating a list of date based on timestamp:
    try:
        _date = list(map(_timestamp_to_datetime, _json["timestamp"]))
    except KeyError:
        return _empty_dataframe()
    # Building the DataFrame with open/high/low/close/adjclose/volume :
    df = pandas.DataFrame(
        {
            "open": _json["indicators"]["quote"][0]["open"],
            "high": _json["indicators"]["quote"][0]["high"],
            "low": _json["indicators"]["quote"][0]["low"],
            "close": _json["indicators"]["quote"][0]["close"],
            "adjclose": _json["indicators"]["adjclose"][0]["adjclose"],
            "volume": _json["indicators"]["quote"][0]["volume"],
            "dividend": 0.0,
            "split": 1.0,
        },
        index=_date,
    )
    # Retrieving dividends:
    try:
        for timestamp, dividend in _json["events"]["dividends"].items():
            df.loc[_timestamp_to_datetime(timestamp), "dividend"] = dividend["amount"]
    except KeyError:
        pass
    # Retrieving splits:
    try:
        for timestamp, split in _json["events"]["splits"].items():
            split_ratio = float(split["numerator"]) / float(split["denominator"])
            df.loc[_timestamp_to_datetime(timestamp), "split"] = split_ratio
    except KeyError:
        pass
    # Flooring index to keep only days:
    df.index = df.index.floor("d")
    return df


def yahoo_historical_data(ticker="", from_date=0, to_date=0, yahoo_session=None):
    """
    Download data from FINANCE.YAHOO.COM a returns a 'DataFrame' object.
    This function mirrors the GET request that is sent by the URL
    `<https://finance.yahoo.com/quote/^AAPL/history>`_ for example.

    Args:
        ticker: Yahoo ticker to download
        from_date: define the starting or finishing dates to download data.
            The order between ``from_date`` and ``to_date`` does not matter.
        to_date: define the starting or finishing dates to download data.
            The order between ``from_date`` and ``to_date`` does not matter.

    Returns:
        Return a ``pandas.DataFrame``.
    """
    if not isinstance(ticker, str):
        logger.warning(
            f"Parameter ticker={ticker}, type={type(ticker)} must "
            f"be a <str> object. A void DataFrame will be return."
        )
        return _empty_dataframe()
    # Get crumb value + headers:
    if yahoo_session is None:
        yahoo_session = pfgs.yahoo_session()
    crumb = yahoo_session.crumb
    cookies = yahoo_session.cookies
    from_date = _to_utc_timestamp(from_date)
    to_date = _to_utc_timestamp(to_date)
    if from_date > to_date:
        (from_date, to_date) = (to_date, from_date)
    to_date = to_date + 86399  # 24h == 86400 seconds
    # Building url requests:
    params = {
        "formatted": True,
        "crumb": crumb,
        "lang": "en-US",
        "region": "US",
        "events": "div|split",
        "includeAdjustedClose": True,
        "interval": "1d",
        "period1": int(from_date),
        "period2": int(to_date),
        "events": "div|split",
        "corsDomain": "finance.yahoo.com",
    }

    # Sending the GET request, first on query1 server, if fail, on query2:
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?"
        f"{urllib.parse.urlencode(params)}"
    )
    logger.debug(f"Sending requests GET {url}")
    try:
        response = requests.get(url, cookies=cookies)
    except (ConnectTimeout, ConnectionError):
        logger.warning("Internet connection seems to be down.")
        return _empty_dataframe()
    if response.status_code != 200:
        logger.debug(
            "Server query1 response was not 200. "
            "Sending the same requests to server https://query2"
        )
        url = (
            f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}?"
            f"{urllib.parse.urlencode(params)}"
        )
        response = requests.get(url, cookies=cookies)
        if response.status_code != 200:
            logger.debug(
                f"Request {url} did not return a valid response. "
                f"A void DataFrame will be return."
            )
            return _empty_dataframe()

    df = _parse_query_to_pandas(response.text)
    logger.debug(f"Request was parsed. {len(df)} value(s) were found.")
    return df
