#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State
HostAddr = "0.0.0.0"
HostPort = 5000
app = Flask(__name__)


@app.teardown_appcontext
def teardown_context(exception):
    """teardown"""
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states_by_id(id=None):
    """display states by id when id is available"""
    states = storage.all("State")
    cities = storage.all("City")
    return render_template(
        "9-states.html",
        states=states,
        cities=cities,
        id=id
        )


if __name__ == "__main__":
    app.run(
        host=HostAddr,
        port=HostPort,
        debug=True
    )
