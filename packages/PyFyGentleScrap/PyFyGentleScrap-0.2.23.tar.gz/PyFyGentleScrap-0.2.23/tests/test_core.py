# coding: utf-8
# !/usr/bin/python3

import pytest
import requests
import requests_mock
from requests.exceptions import ConnectTimeout


def test_ping_yahoo():
    """ Ping Yahoo website to check internet connection is active. """
    url = "https://www.yahoo.com/"
    requests.head(url, timeout=1.0)


def test_mock_ping_yahoo():
    """Using requests_mock to take control over `requests` answers.
    HEAD requests response.text are forced to be `resp`."""
    url = "https://www.yahoo.com/"
    with requests_mock.Mocker() as mock:
        mock.head(url, text="resp")
        result = requests.head(url).text
    assert result == "resp"


def test_simulate_internet_shutdown():
    """Using requests_mock to take control over `requests` answers.
    All requests to yahoo raise a ConnectTimeout exception."""
    url = "https://www.yahoo.com/"
    with requests_mock.Mocker() as mock:
        mock.register_uri(requests_mock.ANY, url, exc=ConnectTimeout)
        with pytest.raises(ConnectTimeout):
            requests.get(url)
