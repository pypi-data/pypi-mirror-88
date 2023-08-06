# coding: utf-8
# !/usr/bin/python3

import logging
import pytest
import pyfygentlescrap as pfgs
import re
import requests_mock
from requests.exceptions import ConnectTimeout
from requests.exceptions import ConnectionError

# from https://requests-mock.readthedocs.io/en/latest/
#      matching.html#regular-expressions


class TestYahooFunctionsWithInternetDisconnected:
    def setup_class(self):
        """ Setting logger to DEBUG mode."""
        logger = logging.getLogger("pyfygentlescrap")
        ch = logging.StreamHandler()
        fmt = logging.Formatter(
            "%(asctime)s %(name)s.%(module)s %(levelname)s: %(message)s",
            datefmt="%Y/%m/%d %I:%M:%S",
        )
        ch.setFormatter(fmt)
        logger.addHandler(ch)
        logger.setLevel(logging.DEBUG)

    @pytest.mark.parametrize(
        "request_error",
        [ConnectTimeout, ConnectionError],
    )
    def test_yahoo_screener_belgium(self, request_error):
        # Belgium has approx 169 equities.
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(requests_mock.ANY, matcher, exc=request_error)
            df = pfgs.yahoo_equity_screener(region="Belgium")
        assert len(df) == 00

    @pytest.mark.parametrize(
        "ticker, day",
        [
            ("^VIX", "2020/01/02"),
            ("^VIX", "2020/01/03"),
            ("^VIX", "2020/01/06"),
            ("^GSPC", "2020/01/06"),
        ],
    )
    @pytest.mark.parametrize(
        "request_error",
        [ConnectTimeout, ConnectionError],
    )
    def test_download_eod_data(self, ticker, day, request_error):
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(requests_mock.ANY, matcher, exc=request_error)
            df = pfgs.yahoo_historical_data(ticker, day, day)
        assert len(df) == 0

    @pytest.mark.parametrize(
        "ticker, fromD, toD",
        [
            ("AAPL", "2020/11/06", "2020/11/02"),
            ("^VIX", "2020/01/03", "2020/01/01"),
        ],
    )
    @pytest.mark.parametrize(
        "request_error",
        [ConnectTimeout, ConnectionError],
    )
    def test_with_inverted_from_date_and_to_date(
        self, ticker, fromD, toD, request_error
    ):
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(requests_mock.ANY, matcher, exc=request_error)
            df = pfgs.yahoo_historical_data(ticker=ticker, from_date=fromD, to_date=toD)
        assert len(df) == 0

    @pytest.mark.parametrize(
        "ticker",
        ["^VIX", "^GSPC", "GC=F", "^FCHI", "AAPL"],
    )
    @pytest.mark.parametrize(
        "request_error",
        [ConnectTimeout, ConnectionError],
    )
    def test_yahoo_ticker(self, ticker, request_error):
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(requests_mock.ANY, matcher, exc=request_error)
            result = pfgs.yahoo_ticker(ticker)
            assert len(result) == 0


# -------------------------------------------------------------------------------------
class TestYahooFunctionsWithInvalidResponse:
    def setup_class(self):
        """ Setting logger to DEBUG mode."""
        logger = logging.getLogger("pyfygentlescrap")
        ch = logging.StreamHandler()
        fmt = logging.Formatter(
            "%(asctime)s %(name)s.%(module)s %(levelname)s: %(message)s",
            datefmt="%Y/%m/%d %I:%M:%S",
        )
        ch.setFormatter(fmt)
        logger.addHandler(ch)
        logger.setLevel(logging.DEBUG)

    @pytest.mark.parametrize("server_response", ["resp", None])
    def test_yahoo_screener_belgium(self, server_response):
        # Belgium has approx 169 equities.
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(requests_mock.ANY, matcher, text=server_response)
            df = pfgs.yahoo_equity_screener(region="Belgium")
        assert len(df) == 0

    @pytest.mark.parametrize(
        "ticker, day",
        [
            ("^VIX", "2020/01/02"),
            ("^VIX", "2020/01/03"),
            ("^VIX", "2020/01/06"),
            ("^GSPC", "2020/01/06"),
        ],
    )
    def test_download_eod_data(self, ticker, day):
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(requests_mock.ANY, matcher, text="resp")
            df = pfgs.yahoo_historical_data(ticker, day, day)
        assert len(df) == 0

    @pytest.mark.parametrize(
        "ticker, fromD, toD",
        [
            ("AAPL", "2020/11/06", "2020/11/02"),
            ("^VIX", "2020/01/03", "2020/01/01"),
        ],
    )
    def test_with_inverted_from_date_and_to_date(self, ticker, fromD, toD):
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(requests_mock.ANY, matcher, text="resp")
            df = pfgs.yahoo_historical_data(ticker=ticker, from_date=fromD, to_date=toD)
        assert len(df) == 0

    @pytest.mark.parametrize(
        "ticker",
        ["^VIX", "^GSPC", "GC=F", "^FCHI", "AAPL"],
    )
    def test_yahoo_ticker(
        self,
        ticker,
    ):
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(requests_mock.ANY, matcher, text="resp")
            result = pfgs.yahoo_ticker(ticker)
            assert len(result) == 0


# -------------------------------------------------------------------------------------
class TestYahooFunctionsWithResponseCode400:
    def setup_class(self):
        self.response = 'Bla Bla CrumbStore":{"crumb":"CrumbXYZ"} Bla Bla'

    @pytest.mark.parametrize(
        "ticker",
        ["^VIX", "^GSPC", "GC=F", "^FCHI", "AAPL"],
    )
    def test_yahoo_ticker(
        self,
        ticker,
    ):
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(
                requests_mock.ANY, matcher, text=self.response, status_code=400
            )
            result = pfgs.yahoo_ticker(ticker)
            assert len(result) == 0

    def test_yahoo_screener_belgium(self):
        # Belgium has approx 169 equities.
        with requests_mock.Mocker() as mock:
            matcher = re.compile(".*yahoo.*")
            mock.register_uri(
                requests_mock.ANY, matcher, text=self.response, status_code=400
            )
            df = pfgs.yahoo_equity_screener(region="Belgium")
        assert len(df) == 00
