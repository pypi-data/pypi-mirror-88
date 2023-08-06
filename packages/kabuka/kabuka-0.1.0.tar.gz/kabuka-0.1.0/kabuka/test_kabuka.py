import os
from pathlib import Path
from unittest import mock
from kabuka import kabuka, get_latest_price


TEST_DATA_DIR = Path(os.path.dirname(os.path.realpath(__file__))) / "test_data"

def test_is_numeric():
    assert not kabuka.is_numeric("abc")
    assert not kabuka.is_numeric("123a")
    assert not kabuka.is_numeric("")
    assert not kabuka.is_numeric("this is not a number")
    assert not kabuka.is_numeric("a123")
    assert not kabuka.is_numeric("a123a")
    assert not kabuka.is_numeric("1a123")
    assert not kabuka.is_numeric("0.0.0.0")
    assert not kabuka.is_numeric("1,234.678")
    assert kabuka.is_numeric("123")
    assert kabuka.is_numeric(".123")
    assert kabuka.is_numeric("123.")
    assert kabuka.is_numeric("123.456")
    assert kabuka.is_numeric("123_456")
    assert kabuka.is_numeric("0.123")
    assert kabuka.is_numeric(".123_456")
    assert kabuka.is_numeric("123_456.")
    assert kabuka.is_numeric("123_456.789_101")


def mocked_requests_get(url):
    class MockedResponse:
        def __init__(self, text):
            self.text = text

    uri = url.replace("https://finance.yahoo.com/quote", str(TEST_DATA_DIR)) + ".html"
    try:
        with open(uri, "rb") as f:
            return MockedResponse(f.read().decode("utf8"))
    except IOError:
        with open(TEST_DATA_DIR / "unknown_symbol.html") as f:
            return MockedResponse(f.read())


@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_get_lastest_price(mock_get_latest_price):
    # stonk
    price = get_latest_price("TSLA")
    assert kabuka.is_numeric(price) and float(price) >= 0

    # ETF
    price = get_latest_price("SPY")
    assert kabuka.is_numeric(price) and float(price) >= 0

    # tokyo stock exchange
    price = get_latest_price("4385.T")
    assert kabuka.is_numeric(price) and float(price) >= 0

    # invalid symbol
    try:
        price = get_latest_price("")
    except ValueError:
        assert True
    else:
        assert False

    # invalid symbol
    try:
        price = get_latest_price("apple.com")
    except ValueError:
        assert True
    else:
        assert False

