#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State
HostAddr = "0.0.0.0"
HostPort = 5000
app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """display all states """
    states = storage.all(State)
    states = dict(sorted(
        states.items(),
        key=lambda item: item[1].name)
    )
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown_context(exception):
    """teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(
        host=HostAddr,
        port=HostPort,
        debug=True
    )
