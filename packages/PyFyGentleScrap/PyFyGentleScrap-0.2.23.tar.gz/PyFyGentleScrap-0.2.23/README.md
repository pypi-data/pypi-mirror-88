# PyFyGentleScrap: gently scrap financial data

## What is it?

**PyFyGentleScrap** is a python package that provide function to scrap financial
data on websites, such as end of day tickers (EOD) list for a particular country or
historical EOD values for a particular ticker.

*Gentle* scrapping means that all web requests are designed to avoid the remote
servers to detect the requests as scraping.

All scrapped data are return as `pandas.DataFrame` to easily compute statistics, or
storing data into a database.

NOTE: **PyFyGentleScrap** package is not affiliated to any website. Please use this
package wisely to avoid to be block.

[![PyPI version](https://badge.fury.io/py/PyFyGentleScrap.svg)](https://pypi.org/project/PyFyGentleScrap/)
[![Pipeline](https://gitlab.com/OlivierLuG/pyfygentlescrap/badges/master/pipeline.svg)](https://gitlab.com/OlivierLuG/pyfygentlescrap)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Flake8](https://img.shields.io/badge/flake8-0%20error-brightgreen)](https://gitlab.com/OlivierLuG/pyfygentlescrap)
[![Coverage](https://gitlab.com/OlivierLuG/pyfygentlescrap/badges/master/coverage.svg)](https://gitlab.com/OlivierLuG/pyfygentlescrap)
[![Documentation](https://readthedocs.org/projects/pyfygentlescrap/badge/?version=latest)](https://readthedocs.org/projects/pyfygentlescrap/badge/?version=latest)


## Installing PyFyGentleScrap

PyFyGentleScrap is available on [PyPi](https://pypi.org/project/PyFyGentleScrap/):
```sh
pip install pyfygentlescrap
```

## Main features

Example of equity download:

```python
>>> import pyfygentlescrap as pfgs
>>> df = pfgs.yahoo_ticker('AAPL')
>>> print(df.columns)
Index(['fullExchangeName', 'fiftyTwoWeekLowChangePercent',
'gmtOffSetMilliseconds', 'regularMarketOpen', 'language',
'regularMarketTime', 'regularMarketChangePercent', 'uuid', 'quoteType',
'regularMarketDayRange', 'fiftyTwoWeekLowChange',
'fiftyTwoWeekHighChangePercent', 'regularMarketDayHigh', 'tradeable',
'currency', 'sharesOutstanding', 'fiftyTwoWeekHigh',
'regularMarketPreviousClose', 'exchangeTimezoneName', 'marketCap',
'fiftyTwoWeekHighChange', 'fiftyTwoWeekRange', 'regularMarketChange',
'firstTradeDateMilliseconds', 'exchangeDataDelayedBy',
'exchangeTimezoneShortName', 'regularMarketPrice', 'fiftyTwoWeekLow',
'marketState', 'market', 'regularMarketVolume', 'quoteSourceName',
'messageBoardId', 'priceHint', 'exchange', 'sourceInterval',
'regularMarketDayLow', 'region', 'shortName', 'triggerable',
'longName'],
dtype='object')
>>> df[['regularMarketOpen', 'regularMarketVolume', 'marketState', 'shortName', 'marketCap']]
regularMarketOpen regularMarketVolume marketState   shortName      marketCap
symbol
AAPL              122.43            81462378      CLOSED  Apple Inc.  2081190313984
```
Example of region EOD download:
```python
>>> df = pfgs.yahoo_equity_screener(region='Belgium')
>>> print(len(df.columns)) # 63 columns containing various data are scrapped
63
>>> print(df[['marketState', 'regularMarketOpen', 'regularMarketPrice']])
marketState regularMarketOpen regularMarketPrice
symbol                                                  
MSF.BR       CLOSED            213.05              211.9
INCO.BR      CLOSED              49.4               49.4
CIS.BR       CLOSED            48.995             44.585
...             ...               ...                ...
PAY.BR       CLOSED               7.5                7.6
TEXF.BR      CLOSED              36.6               36.4
WEB.BR       CLOSED              43.4               40.5

[200 rows x 3 columns]
```

Example of region historical EOD data download for one ticker:
```python
>>> df = pfgs.yahoo_historical_data("AAPL", "2019-08-01", "2019-08-31")
>>> print(df)
                 open       high        low      close   adjclose     volume  dividend  split
2019-08-01  53.474998  54.507500  51.685001  52.107498  50.895054  216071600    0.0000    1.0
2019-08-02  51.382500  51.607498  50.407501  51.005001  49.818211  163448400    0.0000    1.0
2019-08-05  49.497501  49.662498  48.145000  48.334999  47.210331  209572000    0.0000    1.0
2019-08-06  49.077499  49.517502  48.509998  49.250000  48.104046  143299200    0.0000    1.0
2019-08-07  48.852501  49.889999  48.455002  49.759998  48.602177  133457600    0.0000    1.0
2019-08-08  50.049999  50.882500  49.847500  50.857498  49.674141  108038000    0.0000    1.0
2019-08-09  50.325001  50.689999  49.822498  50.247501  49.264809   98478800    0.1925    1.0
2019-08-12  49.904999  50.512501  49.787498  50.119999  49.139793   89927600    0.0000    1.0
2019-08-13  50.255001  53.035000  50.119999  52.242500  51.220791  188874000    0.0000    1.0
2019-08-14  50.790001  51.610001  50.647499  50.687500  49.696201  146189600    0.0000    1.0
2019-08-15  50.865002  51.285000  49.917500  50.435001  49.448643  108909600    0.0000    1.0
2019-08-16  51.070000  51.790001  50.959999  51.625000  50.615368  110481600    0.0000    1.0
2019-08-19  52.654999  53.182499  52.507500  52.587502  51.559048   97654400    0.0000    1.0
2019-08-20  52.720001  53.337502  52.580002  52.590000  51.561501  107537200    0.0000    1.0
2019-08-21  53.247501  53.412498  52.900002  53.160000  52.120346   86141600    0.0000    1.0
2019-08-22  53.297501  53.610001  52.687500  53.115002  52.076225   89014800    0.0000    1.0
2019-08-23  52.357498  53.012501  50.250000  50.660000  49.669239  187272000    0.0000    1.0
2019-08-26  51.465000  51.797501  51.264999  51.622501  50.612915  104174400    0.0000    1.0
2019-08-27  51.965000  52.137501  50.882500  51.040001  50.041805  103493200    0.0000    1.0
2019-08-28  51.025002  51.430000  50.830002  51.382500  50.377613   63755200    0.0000    1.0
2019-08-29  52.125000  52.330002  51.665001  52.252499  51.230591   83962000    0.0000    1.0
2019-08-30  52.540001  52.612499  51.799999  52.185001  51.164417   84573600    0.0000    1.0
```

## Documentation

See the full documentation at:
https://pyfygentlescrap.readthedocs.io/en/latest/

## License
[MIT License](https://gitlab.com/OlivierLuG/pyfygentlescrap/-/blob/master/LICENSE)
