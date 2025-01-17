#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask
HostAddr = "0.0.0.0"
HostPort = 5000
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """display text"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """display text"""
    return "HBNB"


if __name__ == "__main__":
    app.run(
        host=HostAddr,
        port=HostPort,
        debug=True
    )
