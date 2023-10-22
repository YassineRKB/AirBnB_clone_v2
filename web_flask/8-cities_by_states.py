#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State
HostAddr = "0.0.0.0"
HostPort = 5000
app = Flask(__name__, template_folder="templates")


@app.route('/cities_by_states', strict_slashes=False)
def states_list():
    """display all cities by states"""
    states = storage.all(State)
    states = dict(sorted(
        states.items(),
        key=lambda item: item[1].name)
    )
    return render_template("8-cities_by_states.html", states=states)


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
