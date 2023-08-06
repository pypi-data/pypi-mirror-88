# coding: utf-8
# !/usr/bin/python3

import datetime as dt
import pytest
import pyfygentlescrap as pfgs


@pytest.mark.parametrize(
    "input_str, tzone, expected",
    [
        ("1970-01-01", None, 0),
        ("1970/01/01", None, 0),
        ("1970-01-01", "Europe/Paris", -3600),
        ("1970-01-01 00:00:01", None, 1),
        ("1970-01-01 00:00:00", None, 0),
        ("2020-01-01", None, 1577836800),
        ("2020-02-15 20:36:53", None, 1581799013),
        ("not-a-valid-datetime", None, 0),
        ("5", None, 0),
        (0.0, None, 0),
        (5.0, None, 5),
        (1581799013, None, 1581799013),
        (dt.date(1970, 1, 1), None, 0),
        (dt.datetime(1970, 1, 1), None, 0),
        (dt.datetime(1970, 1, 1, 12, 0, 0), None, 43200),
        (dt.date(2020, 1, 1), None, 1577836800),
        (dt.datetime(2020, 2, 15, 20, 36, 53), None, 1581799013),
        ("1677-09-21 00:12:43", None, 0),  # below LBound
        ("1677-09-21 00:12:44", None, -9223372036),  # minimum datetime
        ("2262-04-11 23:47:17", None, 0),  # above UBound
        ("2262-04-11 23:47:16", None, 9223372036),  # maximum datetime
    ],
)
def test_to_utc_timestamp(input_str, tzone, expected):
    """test of function '_to_utc_timestamp' from various objects."""
    result = pfgs.yahoo.yahoo_shared._to_utc_timestamp(input_str, tzone)
    assert result == expected


@pytest.mark.parametrize(
    "timestamp, tzone, expected",
    [
        (0, None, dt.datetime(1970, 1, 1, 0, 0, 0)),
        (-3600, "Europe/Paris", dt.datetime(1970, 1, 1, 0, 0, 0)),
        ("not-a-valid-datetime", None, None),
        (9223372036, None, dt.datetime(2262, 4, 11, 23, 47, 16)),
        (-9223372036, None, dt.datetime(1677, 9, 21, 0, 12, 44)),
        (999999999999, None, None),  # above UBound
    ],
)
def test_timestamp_to_datetime(timestamp, tzone, expected):
    """ Test of function '_timestamp_to_datetime' from various objects."""
    result = pfgs.yahoo.yahoo_shared._timestamp_to_datetime(timestamp, tzone)
    assert result == expected
