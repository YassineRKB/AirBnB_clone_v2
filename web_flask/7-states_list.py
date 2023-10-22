#!/usr/bin/python3
"""script that starts a Flask web application"""

from models import storage
from models.state import State
from flask import Flask, render_template
HostAddr = "0.0.0.0"
HostPort = 5000
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states_list')
def states_list():
    """display all states """
    states = storage.all(State)
    states = dict(sorted(
        states.items(),
        key=lambda item: item[1].name)
    )
    return render_template("7-states_list.html", states=states)


if __name__ == "__main__":
    app.run(
        host=HostAddr,
        port=HostPort,
        debug=True
    )
