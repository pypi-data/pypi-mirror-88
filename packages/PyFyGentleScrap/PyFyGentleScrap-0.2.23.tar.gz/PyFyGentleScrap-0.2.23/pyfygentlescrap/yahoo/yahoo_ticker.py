# coding: utf-8
# !/usr/bin/python3

import json
import logging
import pandas
import pyfygentlescrap as pfgs
import requests
import urllib

from json.decoder import JSONDecodeError
from requests.exceptions import ConnectTimeout
from requests.exceptions import ConnectionError

logger = logging.getLogger(__name__)


def yahoo_ticker(ticker="", yahoo_session=None):
    """
    Download live or delayed data for a single ticker, then returns
    a `DataFrame` object.
    This function mirrors the GET request that is sent by the URL
    `<https://finance.yahoo.com/quote/^AAPL/>`_ for example.
    If the `ticker` is not valid or if the GET request fails, then
    the returned value is a void DataFrame.

    Parameters:
        ticker (str): Yahoo ticker to download
        yahoo_session (pfgs.yahoo_session, optional):  Existing yahoo session.
            If no yahoo_session is provided, the function will open one for the
            duration of the function execution. The latter session will be lost
            when `yahoo_historical_data` function exit. For large data
            scrapping, the use of `yahoo_session` is higly recommended to reuse
            existing cookies and crumb values. It will also reduce the cpu
            usage.

    Returns:
        Return a ``pandas.DataFrame``. If the function fails, a void DataFrame
        is returned. No exception is raised.

    Example:
        The following example shows the download of the ticker AAPL. Note that
        for live or EOD data, the following columns are of particular interest:
        ``regularMarketTime``, ``regularMarketOpen``, ``regularMarketDayHigh``,
        ``regularMarketDayLow``, ``regularMarketPrice``.

        The column ``regularMarketTime`` returns an epoch timestamp for the
        last known quotation (live or delayed).

        The column ``marketState`` returns ``OPENED`` or ``CLOSED``.

        If this function is used for database feed, a quality check can be
        performed thanksfully to the colum ``regularMarketPreviousClose``.

        >>> import pyfygentlescrap as pfgs
        >>> print(df.columns)
        Index(['fullExchangeName', 'fiftyTwoWeekLowChangePercent',
               'gmtOffSetMilliseconds', 'regularMarketOpen', 'language',
               'regularMarketTime', 'regularMarketChangePercent', 'uuid',
               'quoteType', 'regularMarketDayRange', 'fiftyTwoWeekLowChange',
               'fiftyTwoWeekHighChangePercent', 'regularMarketDayHigh',
               'tradeable', 'currency', 'sharesOutstanding',
               'fiftyTwoWeekHigh', 'regularMarketPreviousClose',
               'exchangeTimezoneName', 'fiftyTwoWeekHighChange', 'marketCap',
               'regularMarketChange', 'fiftyTwoWeekRange',
               'firstTradeDateMilliseconds', 'exchangeDataDelayedBy',
               'exchangeTimezoneShortName','regularMarketPrice',
               'fiftyTwoWeekLow', 'marketState', 'regularMarketVolume',
               'market', 'quoteSourceName','messageBoardId', 'priceHint',
               'regularMarketDayLow', 'exchange', 'sourceInterval',
               'region', 'shortName', 'triggerable', 'longName'],
              dtype='object')

    """
    if not isinstance(ticker, str):
        logger.warning(
            f"Parameter ticker={ticker}, type={type(ticker)} must "
            f"be a <str> object. A void DataFrame will be return."
        )
        return pandas.DataFrame()
    # Get crumb value + headers:
    if yahoo_session is None:
        try:
            yahoo_session = pfgs.yahoo_session()
        except (ConnectTimeout, ConnectionError):
            return pandas.DataFrame()
    crumb = yahoo_session.crumb
    cookies = yahoo_session.cookies

    # Building url requests:
    params = {
        "formatted": True,
        "crumb": crumb,
        "lang": "en-US",
        "region": "US",
        "symbols": ticker,
        "fields": "messageBoardId,longName,shortName,marketCap,underlyingSymbol,"
        "underlyingExchangeSymbol,headSymbolAsString,regularMarketPrice,"
        "regularMarketChange,regularMarketChangePercent,"
        "regularMarketVolume,uuid,regularMarketOpen,fiftyTwoWeekLow,"
        "fiftyTwoWeekHigh,toCurrency,fromCurrency,toExchange,fromExchange",
        "corsDomain": "finance.yahoo.com",
    }

    # Sending the GET request, first on query1 server, if fail, on query2:
    url_path = "https://query1.finance.yahoo.com/v7/finance/quote"
    url = f"{url_path}?{urllib.parse.urlencode(params)}"
    logger.debug(f"Sending requests GET {url}")
    try:
        response = requests.get(url, cookies=cookies)
    except (ConnectTimeout, ConnectionError):
        logger.warning("Internet connection seems to be down.")
        return pandas.DataFrame()
    if response.status_code != 200:
        logger.debug(
            "Server query1 response was not 200. "
            "Sending the same requests to server https://query2"
        )
        url_path = "https://query2.finance.yahoo.com/v7/finance/quote"
        url = f"{url_path}?{urllib.parse.urlencode(params)}"
        response = requests.get(url, cookies=cookies)
        if response.status_code != 200:
            logger.debug(
                f"Request {url} did not return a valid response. "
                f"A void DataFrame will be return."
            )
            return pandas.DataFrame()

    # Parsing results:
    try:
        _json = json.loads(response.text)
    except JSONDecodeError:
        logger.debug(
            "Request did not return a valid response. "
            "A void DataFrame will be return."
        )
        return pandas.DataFrame()
    try:
        _json = _json["quoteResponse"]["result"][0]
    except IndexError:
        logger.debug(
            f"Ticker {ticker} did not return a valid response. "
            f"A void DataFrame will be return."
        )
        return pandas.DataFrame()

    # converting _json to pandas:
    df = pandas.DataFrame.from_dict(_json)
    df = df.loc[["raw"]]
    df.index = df["symbol"]
    df = df.drop(columns=["symbol"])
    return df
