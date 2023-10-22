#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask, render_template
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


@app.route('/python')
@app.route('/python/<text>')
def python_text(text="is cool"):
    """display Python parameter text"""
    result = 'Python {}'.format(text.replace('_', ' '))
    return result


@app.route('/number/<int:n>')
def text_if_int(n):
    """display int parameter text"""
    result = "{:d} is a number".format(n)
    return result


@app.route("/number_template/<int:n>")
def number_template_n(n):
    """display int parameter text using template"""
    return render_template("5-number.html", intnum=n)


if __name__ == "__main__":
    app.run(
        host=HostAddr,
        port=HostPort,
        debug=True
    )
