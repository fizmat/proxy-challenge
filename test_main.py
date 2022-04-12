from requests import get

from main import modify


def test_modify():
    s = 'Hello World'
    assert modify(s) == s
    s = get('https://news.ycombinator.com/item?id=13713480').text
    assert modify(s) == s
