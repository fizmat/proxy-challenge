import re
from urllib.parse import urlsplit, urlunsplit

from flask import Flask, request
from requests import get
from bs4 import BeautifulSoup
import nltk
from nltk import NLTKWordTokenizer, PunktSentenceTokenizer

app = Flask(__name__)

proxy_ip = '127.0.0.1'
proxy_port = 8232
upstream_domain = 'news.ycombinator.com'
upstream = 'https://' + upstream_domain
modify_word_length = 6
append_character = '™'


def modify_href(href, upstream_loc=upstream_domain):
    scheme, loc, path, query, fragment = urlsplit(href)
    print([scheme, loc, path, query, fragment])
    if loc == upstream_loc:
        return urlunsplit(['', '', path, query, fragment])
    else:
        return href


def modify_string(text, word_length=modify_word_length):
    results = []
    prev_sentence_end = 0
    for sentence_start, sentence_end in PunktSentenceTokenizer().span_tokenize(text):
        results.append(text[prev_sentence_end:sentence_start])
        sentence = text[sentence_start:sentence_end]
        prev_end = 0
        for start, end in NLTKWordTokenizer().span_tokenize(sentence):
            fragment = sentence[prev_end:end]
            if end - start == word_length:
                fragment += append_character
            results.append(fragment)
            prev_end = end
        results.append(sentence[prev_end:])
        prev_sentence_end = sentence_end
    results.append(text[prev_sentence_end:])
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
