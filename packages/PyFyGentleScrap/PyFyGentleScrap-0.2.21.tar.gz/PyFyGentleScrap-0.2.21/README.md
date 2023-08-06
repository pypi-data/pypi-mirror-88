# PyFyGentleScrap: gently scrap financial data

DISCLAIMER:
When using **PyFyGentleScrap**, you implicitely accept cookies and third party policies
of the scrapped websites.

## What is it?

**PyFyGentleScrap** is a python module to scrap financial data. It's goal is to fetch
financial data from websites and return them as *pandas* data.

*Gentle* scrapping means that all web requests are designed to avoid the servers
to detect the requests as scraping. This also means that cookies and licenses are
accepted.

## Main features

### Yahoo scrapping (https://finance.yahoo.com)
Two functions are available to scrap yahoo :
 - `yahoo_equity_screener(regions=['Belgium', 'United States'])`, which will 
basically return EOD values (open/high/low/close/volume) + many additionnal
informations.
 - ![not_developped](https://img.shields.io/badge/-not%20developped%20yet-critical) `yahoo_historical_data(equities=['AAPL'])`

_ [https://finance.yahoo.com/screener/](https://finance.yahoo.com/screener/)



## Main dependencies

- [Firefox](https://www.mozilla.org/fr/firefox/)
- [Geckodriver](https://github.com/mozilla/geckodriver/releases)
- [Selenium](https://pypi.org/project/selenium/)
- [Requests](https://github.com/psf/requests)
- [Pandas](https://github.com/pandas-dev/pandas)

## Guide to contribute to the code

All contributions are welcome. If you think you've discovered an issue, please read
[this stackoverflow article](https://stackoverflow.com/help/minimal-reproducible-example)
for tips on writing a good bug report.

1. Forking

```sh
git clone https://gitlab.com/your-user-name/pyfygentlescrap.git
cd pyfygentlescrap
git remote add upstream https://gitlab.com/your-user-name/pyfygentlescrap
```

2. Set a virtual environment
3. Install main and development dependencies:

```sh
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
```
Note: Use the `--upgrade` option to update package to the last stable version.

4. (optionnal) Run tests to check that everything is working fine:

```sh
pytest
```

5. Create a new branch, test it, check linting, pull it:

```sh
git branch my_super_branch
git checkout my_super_branch
```
Code a super functionnality, then test it:
```sh
# linting:
black pyfygentlescrap
flake8 pyfygentlescrap
# building documention:
cd docs && make html
# testing, coverage:
python3 -m pytest # or simply `pytest`
python3 -m coverage run --source=. -m pytest && python3 -m coverage report -m
```
