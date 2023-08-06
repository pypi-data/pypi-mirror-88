import requests
from bs4 import BeautifulSoup


def is_numeric(val: str) -> bool:
    """ Returns True if the input value can be casted to numeric type

    "123.456" -> True
    "pi" -> False

    Args:
        val (str): input value to test

    Returns:
        bool: True if `val` can be casted to numeric type
    """
    try:
        float(val)
        return True
    except:
        return False


def get_latest_price(ticker_symbol: str) -> str:
    """ get lastest stock price from Yahoo Finance

    Args:
        ticker_symbol (str): stock ticker, e.g."TSLA"

    Raises:
        ValueError: raised if the input ticker symbol is invalid or unavailable.

    Returns:
        str: price in str, e.g. '420.69'
    """
    url = f"https://finance.yahoo.com/quote/{ticker_symbol}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    price_dom = soup.find("span", {"data-reactid": 32})
    if price_dom and price_dom.contents:
        price = price_dom.contents.pop().replace(",", "")
        if is_numeric(price):
            return price
    raise ValueError(f"No results for symbol `{ticker_symbol}`")
