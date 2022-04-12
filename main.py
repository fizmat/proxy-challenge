from flask import Flask, request, escape

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello(path):
    return escape(request.url)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8232)
