# coding: utf-8
# !/usr/bin/python3

import json
import logging
import pandas
import requests
import urllib

from json.decoder import JSONDecodeError
from pyfygentlescrap.yahoo.yahoo_shared import _get_yahoo_cookies_and_crumb


logger = logging.getLogger(__name__)

# List of Regions as defined in the yahoo screener, and its associated code:
yahoo_regions = {
    "Argentina": "ar",
    "Austria": "at",
    "Australia": "au",
    "Belgium": "be",
    "Bahrain": "bh",
    "Brazil": "br",
    "Canada": "ca",
    "Switzerland": "ch",
    "Chile": "cl",
    "China": "cn",
    "Czech Republic": "cz",
    "Germany": "de",
    "Denmark": "dk",
    "Egypt": "eg",
    "Spain": "es",
    "Finland": "fi",
    "France": "fr",
    "United Kingdom": "gb",
    "Greece": "gr",
    "Hong Kong": "hk",
    "Hungary": "hu",
    "Indonesia": "id",
    "Ireland": "ie",
    "Israel": "il",
    "India": "in",
    "Italy": "it",
    "Jordan": "jo",
    "Japan": "jp",
    "South Korea": "kr",
    "Kuwait": "kw",
    "Sri Lanka": "lk",
    "Luxembourg": "lu",
    "Mexico": "mx",
    "Malaysia": "my",
    "Netherlands": "nl",
    "Norway": "no",
    "New Zealand": "nz",
    "Peru": "pe",
    "Philippines": "ph",
    "Pakistan": "pk",
    "Poland": "pl",
    "Portugal": "pt",
    "Qatar": "qa",
    "Russia": "ru",
    "Sweden": "se",
    "Singapore": "sg",
    "Suriname": "sr",
    "French Southern Territories": "tf",
    "Thailand": "th",
    "Timor-Leste": "tl",
    "Tunisia": "tn",
    "Turkey": "tr",
    "Taiwan": "tw",
    "United States": "us",
    "Venezuela": "ve",
    "Vietnam": "vn",
    "South Africa": "za",
}


def _parse_query_to_pandas(json_response):
    """
    pre-parsed requests to convert the data into a ``pandas.DataFrame``.

    Args:
        json_response: a valid json response

    Returns:
        DataFrame
    """
    df = pandas.DataFrame()
    quotes = json_response["finance"]["result"][0]["quotes"]
    for quo in quotes:
        df1 = pandas.DataFrame.from_dict(quo)
        df1 = df1.loc[["raw"]]
        df1.index = df1["symbol"]
        df1 = df1.drop(columns=["symbol"])
        df = pandas.concat([df, df1])
    return df


def _get_query_response(params, headers, encoded_body):
    """Sending the GET request, first on query1 server, if fail, on query2."""
    url = (
        f"https://query1.finance.yahoo.com/v1/finance/screener?"
        f"{urllib.parse.urlencode(params)}"
    )
    logger.debug(f"Sending requests POST {url}")
    response = requests.post(url, headers=headers, data=encoded_body)
    if response.status_code == 200:
        return response
    logger.debug(
        f"Server query1 response was {response.status_code} (not 200). "
        f"Sending the same requests to server https://query2"
    )
    url = (
        f"https://query2.finance.yahoo.com/v1/finance/screener?"
        f"{urllib.parse.urlencode(params)}"
    )
    response = requests.post(url, headers=headers, data=encoded_body)
    if response.status_code == 200:
        return response
    logger.debug(
        f"Request {url} did not return a valid response on both "
        f"query1 and query2 servers (second response: {response.status_code})."
    )
    return None


def yahoo_equity_screener(region="France", session=None):
    """
    Downloads live (or delayed) equities data given a region. This function
    mirrors the GET request that is returned by yahoo screener available at
    `<https://finance.yahoo.com/screener/new.>`_. The result type is a
    `pandas.DataFrame`. If the region parameter is not a valid country, order
    if the function fails for whaterver reason, the function will return a
    void DataFrame. No exception is raised.

    Args:
        region (str): Region to scrap. The full list is available at
            `<https://finance.yahoo.com/screener/new.>`_.
        yahoo_session (pfgs.yahoo_session, optional):  Existing yahoo
            session. If no yahoo_session is provided, the function
            will open one for the duration of the function execution.
            The latter session will be lost when `yahoo_historical_data`
            function exit. For large data scrapping, the use of
            `yahoo_session` is higly recommended to reuse existing
            cookies and crumb values. It will also reduce the cpu
            usage.

    Returns:
        `pandas.DataFrame` containing all the scrapped data.

    Example:
        The following example shows the download of all the tickers for
        Belgium. The returned DataFrame colums are particularely interesting:

            - ``regularMarketOpen``, ``regularMarketDayHigh``,
                ``regularMarketDayLow``, ``regularMarketPrice``: theses columns
                gives EOD data. Note that `regularMarketPrice` returns the
                live or delayed data if the market is openned.
            - ``regularMarketVolume``: volume for the current session.
            - ``marketCap``: capitalization.
            - ``marketState``: current market status.
            - ``regularMarketPreviousClose``: close for the previous session.

        >>> import pyfygentlescrap as pfgs
        >>> df = pfgs.yahoo_equity_screener(region='Belgium')
        >>> print(len(df))  # 200 values are returned
        200
        >>> print(df.columns)
        Index(['twoHundredDayAverageChangePercent',
               'fiftyTwoWeekLowChangePercent', 'language',
               'regularMarketDayRange', 'regularMarketDayHigh',
               'twoHundredDayAverageChange', 'askSize', 'twoHundredDayAverage',
               'bookValue', 'marketCap', 'fiftyTwoWeekHighChange',
               'fiftyTwoWeekRange', 'fiftyDayAverageChange',
               'firstTradeDateMilliseconds', 'exchangeDataDelayedBy',
               'averageDailyVolume3Month', 'trailingAnnualDividendRate',
               'fiftyTwoWeekLow', 'regularMarketVolume', 'market',
               'messageBoardId', 'priceHint', 'regularMarketDayLow',
               'exchange', 'sourceInterval', 'region', 'shortName',
               'fiftyDayAverageChangePercent', 'fullExchangeName',
               'financialCurrency', 'gmtOffSetMilliseconds',
               'regularMarketOpen', 'regularMarketTime',
               'regularMarketChangePercent', 'quoteType',
               'trailingAnnualDividendYield', 'averageDailyVolume10Day',
               'fiftyTwoWeekLowChange', 'fiftyTwoWeekHighChangePercent',
               'trailingPE', 'tradeable', 'currency', 'sharesOutstanding',
               'regularMarketPreviousClose', 'fiftyTwoWeekHigh',
               'exchangeTimezoneName', 'bidSize', 'regularMarketChange',
               'fiftyDayAverage', 'exchangeTimezoneShortName', 'marketState',
               'regularMarketPrice', 'ask', 'epsTrailingTwelveMonths', 'bid',
               'priceToBook', 'triggerable', 'longName',
               'earningsTimestampEnd', 'epsForward', 'earningsTimestampStart',
               'forwardPE', 'earningsTimestamp', 'newListingDate'],
              dtype='object')
        >>> print(df[['shortName', 'marketCap', 'exchange', 'currency']])
                           shortName      marketCap exchange currency
        symbol
        MSF.BR    MICROSOFT CORP SPL  1637461000192      BRU      USD
        INCO.BR           INTEL CORP   205712080896      BRU      USD
        CIS.BR      CISCO SYSTEM INC   186497761280      BRU      USD
        BOEI.BR       BOEING COMPANY   125048283136      BRU      USD
        ABI.BR              AB INBEV   113554939904      BRU      EUR
        ...                      ...            ...      ...      ...
        ROU.BR              ROULARTA      181946000      BRU      EUR
        EXM.BR                 EXMAR      162237696      BRU      EUR
        TISN.BR              TISCALI      161285680      BRU      EUR
        INCLU.BR                 NaN      159204448      BRU      EUR
        TEXF.BR                TEXAF      131889560      BRU      EUR
        [200 rows x 4 columns]
    """

    if not isinstance(region, str):
        logger.warning(
            f"Parameter region={region}, type={type(region)} must "
            f"be a <str> object. A void DataFrame will be return."
        )
        return pandas.DataFrame()
    try:
        region = yahoo_regions[region]
    except KeyError:
        logger.warning(
            f"Region {region} is not a valid country. A void DataFrame will be return."
        )
        return pandas.DataFrame()

    # Get crumb value + cookies:
    yahoo_request_parameters = _get_yahoo_cookies_and_crumb()
    crumb = yahoo_request_parameters["crumb"]
    if crumb == "":
        logger.warning(
            "Internet connection seems to be down."
            "The screener will return a void DataFrame."
        )
        return pandas.DataFrame()
    cookies = []
    for cookie in yahoo_request_parameters["cookies"]:
        cookies.append(f"{cookie.name}={cookie.value}")
    cookies = "; ".join(cookies)

    # building requests parameters:
    params = {
        "crumb": crumb,
        "lang": "en-US",
        "region": "US",
        "formatted": True,
        "corsDomain": "finance.yahoo.com",
    }
    # building headers + body:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) "
        "Gecko/20100101 Firefox/83.0",
        "Connection": "keep-alive",
        "Expires": "-1",
        "Upgrade-Insecure-Requests": "1",
        "Cookie": cookies,
    }
    body = {
        "size": 25,
        "offset": 0,
        "sortField": "intradaymarketcap",
        "sortType": "DESC",
        "quoteType": "EQUITY",
        "topOperator": "AND",
        "query": {
            "operator": "AND",
            "operands": [
                {
                    "operator": "or",
                    "operands": [
                        {
                            "operator": "EQ",
                            "operands": ["region", region],
                        }
                    ],
                }
            ],
        },
        "userId": "",
        "userIdType": "guid",
    }
    encoded_body = json.dumps(body).encode("UTF-8")

    # POST request on both query servers:
    response = _get_query_response(params, headers, encoded_body)
    if response is None:
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

    total = _json["finance"]["result"][0]["total"]  # Total number of equities
    body["offset"] = 0
    body["size"] = 100
    encoded_body = json.dumps(body).encode("UTF-8")
    logger.debug(f"Yahoo POST response says {total} are available.")

    # Looping to scrap all equities:
    df = pandas.DataFrame()
    while body["offset"] < total:
        # POST request on both query servers:
        response = _get_query_response(params, headers, encoded_body)
        # Parsing results:
        _json = json.loads(response.text)
        _df = _parse_query_to_pandas(_json)
        df = pandas.concat([df, _df])
        body["offset"] += 100

    df.drop_duplicates()
    return df
