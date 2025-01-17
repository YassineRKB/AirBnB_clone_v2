#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask
HostAddr = "0.0.0.0"
HostPort = 5000
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_hbnb():
    """display text"""
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """display text"""
    return "HBNB"


@app.route('/c/<text>')
def c_text(text):
    """display c parameter text"""
    result = "C {}".format(text.replace('_', ' '))
    return result


if __name__ == "__main__":
    app.run(
        host=HostAddr,
        port=HostPort,
        debug=True
    )
