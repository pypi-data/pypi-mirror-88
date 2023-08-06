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
    """ toto"""
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
