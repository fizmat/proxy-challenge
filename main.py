import re
from urllib.parse import urlsplit, urlunsplit

from flask import Flask, request
from requests import get
from bs4 import BeautifulSoup
from nltk import NLTKWordTokenizer

app = Flask(__name__)

proxy_ip = '127.0.0.1'
proxy_port = 8232
upstream_domain = 'news.ycombinator.com'
upstream = 'https://' + upstream_domain
modify_word_length = 6
append_character = '™'


def modify_href(href, proxy_loc=f'{proxy_ip}:{proxy_port}', upstream_loc=upstream_domain):
    scheme, loc, path, query, fragment = urlsplit(href)
    print([scheme, loc, path, query, fragment])
    if loc == upstream_loc:
        return urlunsplit(['http', proxy_loc, path, query, fragment])
    else:
        return href


def modify_string(s, word_length=modify_word_length):
    prev_b = 0
    results = []
    for a, b in NLTKWordTokenizer().span_tokenize(s):
        fragment = s[prev_b:b]
        if b - a == word_length:
            fragment += append_character
        results.append(fragment)
        prev_b = b
    results.append(s[prev_b:])
    return ''.join(results)


def modify_html(text):
    soup = BeautifulSoup(text, 'lxml')
    body = soup.find('body')
    for s in body.find_all(string=True):
        s.replace_with(modify_string(str(s)))
    for a in body.find_all('a', href=re.compile(upstream_domain)):
        a['href'] = modify_href(a['href'])
    return soup.decode(formatter='html5')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello(path):
    r = get(f'{upstream}/{path}', params=request.args)
    content_type = r.headers.get('content-type')
    if content_type.startswith('text/html;') or content_type == 'text/html':
        return modify_html(r.text)
    else:
        return r.content


if __name__ == '__main__':
    app.run(host=proxy_ip, port=proxy_port)
