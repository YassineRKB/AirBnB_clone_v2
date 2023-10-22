#!/usr/bin/python3
"""script that starts a Flask web application"""

from models import storage
from models.state import State
from models.city import City
from flask import Flask, render_template
HostAddr = "0.0.0.0"
HostPort = 5000
app = Flask(__name__, template_folder="templates")


@app.teardown_appcontext
def teardown_context(exception):
    """teardown"""
    storage.close()


@app.route("/states", strict_slashes=False)
def states():
    """display all cities by states"""
    states = storage.all(State)
    states = dict(sorted(
        states.items(),
        key=lambda item: item[1].name)
        )
    return render_template(
        "9-states.html",
        missingRes=False,
        data=states,
        id=None
        )


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """display all cities by state id"""
    state = storage.search(State, id=id)
    if state is None:
        return render_template(
            "9-states.html",
            missingRes=True,
            data=states
            )
    citiesList = storage.all(City)
    cities = {}
    for key, city in citiesList.items():
        if state.id == city.state_id:
            cities[key] = city
    cities = dict(sorted(
        cities.items(),
        key=lambda item: item[1].name)
        )
    return render_template(
        "9-states.html",
        missingRes=False,
        name=state.name,
        data=cities,
        id=1
        )


if __name__ == "__main__":
    app.run(
        host=HostAddr,
        port=HostPort,
        debug=True
    )
