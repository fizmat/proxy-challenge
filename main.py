from flask import Flask, request
from requests import get
from bs4 import BeautifulSoup

app = Flask(__name__)

upstream = 'https://news.ycombinator.com'


def modify_string(s):
    return s


def modify_html(text):
    soup = BeautifulSoup(text, 'lxml')
    body = soup.find('body')
    for s in body.find_all(string=True):
        s.replace_with(modify_string(str(s)))
    return soup.decode(formatter='html5')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello(path):
    r = get(f'{upstream}/{path}', params=request.args)
    if r.headers.get('content-type') == 'text/html':
        return modify_html(r.text)
    else:
        return r.content


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8232)
