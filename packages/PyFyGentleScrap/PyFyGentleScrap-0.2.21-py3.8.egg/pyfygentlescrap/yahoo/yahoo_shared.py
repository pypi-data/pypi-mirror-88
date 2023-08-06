# coding: utf-8
# !/usr/bin/python3

import datetime as dt
import logging
import pandas
import pyfygentlescrap as pfgs
import pytz
import re
import requests
from requests.exceptions import ConnectTimeout
from requests.exceptions import ConnectionError


logger = logging.getLogger(__name__)


class yahoo_session:
    def __init__(self, url="https://finance.yahoo.com/screener/new"):
        logger.debug("Initializing Yahoo session: finding crumb value + cookies")
        getYahoo = _get_yahoo_cookies_and_crumb(url)
        self.crumb = getYahoo["crumb"]
        logger.debug(f"Found crumb value: {self.crumb}")
        self.cookies = getYahoo["cookies"]
        self.cookies_msg = "; ".join([f"{x.name}={x.value}" for x in self.cookies])
        logger.debug(f"Found {len(self.cookies)} cookies: {self.cookies_msg}")

    def yahoo_equity_screener(self, region):
        return pfgs.yahoo_equity_screener(region, self)

    def yahoo_historical_data(self, ticker, from_date, to_date):
        return pfgs.yahoo_historical_data(ticker, from_date, to_date, self)

    def yahoo_ticker(self, ticker):
        return pfgs.yahoo_ticker(ticker, self)


def _get_yahoo_cookies_and_crumb(url="https://finance.yahoo.com/screener/new"):
    """
    Open https://finance.yahoo.com/screener/new by default, or any other
    adress, and returns a dict containing cookies and the crumb value.
    """
    with requests.session():
        header = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) "
            "Gecko/20100101 Firefox/77.0",
            "Connection": "keep-alive",
            "Expires": "-1",
            "Upgrade-Insecure-Requests": "1",
        }
        try:
            response = requests.get(url, headers=header)
        except (ConnectTimeout, ConnectionError):
            logger.warning("Internet connection seems to be down.")
            return {"crumb": "", "cookies": ""}
        txt = response.content.decode("utf-8")
        crumb = re.findall('"CrumbStore":{"crumb":"(.+?)"}', txt)
        crumb = crumb[0] if len(crumb) > 0 else ""
        if ("\\u002" in crumb) or (crumb == ""):
            try:
                return _get_yahoo_cookies_and_crumb(url)
            except RecursionError:
                logger.warning("No valid crumb was found (RecursionError).")
                return {"crumb": "", "cookies": ""}
        return {"crumb": crumb, "cookies": response.cookies}


def _to_utc_timestamp(date_arg, tzone="UTC"):
    """
    Returns the timestamp of an object given a timezone. This function is
    particularly used to define starting/ending timestamp of yahoo.com
    historical data url.

    Args:
        date_arg: Object to convert.
        tzone: timezone as string, the list is defined in the ``pytz`` module.
            Type ``pytz.all_timezones`` to see all the available tz.

    Returns:
        A timestamp value (type: `int`).
    """
    if tzone is None:
        tzone = "UTC"
    try:
        if isinstance(date_arg, (float, int)):
            return date_arg
        elif isinstance(date_arg, dt.datetime):
            return date_arg.replace(tzinfo=pytz.timezone(tzone)).timestamp()
        elif isinstance(date_arg, dt.date):
            ts = dt.datetime.combine(
                date_arg, dt.time(0, 0), tzinfo=pytz.timezone(tzone)
            )
            return ts.timestamp()
        return dt.datetime.timestamp(pandas.Timestamp(date_arg, tz=tzone))
    except ValueError:
        return 0


def _timestamp_to_datetime(timestamp, tzone="UTC"):
    """
    Returns the datetime an object given a timestamp. This function gives
    the reverse value of `_to_utc_timestamp`.

    Args:
        timestamp: Timestamp to be converted
        tzone: timezone as string, the list is defined in the ``pytz`` module.
            Type ``pytz.all_timezones`` to see all the available tz.

    Returns:
        A datetime object.
    """
    # Note, the localization has yet to be programmed:
    if tzone is None:
        tzone = "UTC"
    try:
        date = dt.datetime.fromtimestamp(int(timestamp))
    except ValueError:
        return None
    date = date.astimezone(pytz.timezone(tzone)).replace(tzinfo=None)
    return date
