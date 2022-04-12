from flask import Flask, request
from requests import get
from bs4 import BeautifulSoup
from nltk import NLTKWordTokenizer

app = Flask(__name__)

upstream = 'https://news.ycombinator.com'
modify_word_length = 6
append_character = '™'


def modify_string(s, word_length=modify_word_length):
    prev_b = 0
    results = []
    for a, b in NLTKWordTokenizer().span_tokenize(s):
        fragment = s[prev_b:b]
        if b-a == word_length:
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
    app.run(host='127.0.0.1', port=8232)
