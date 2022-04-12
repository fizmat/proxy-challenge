from flask import Flask, request
from requests import get

app = Flask(__name__)

upstream = 'https://news.ycombinator.com'


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello(path):
    r = get(f'{upstream}/{path}', params=request.args)
    return r.content


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8232)
