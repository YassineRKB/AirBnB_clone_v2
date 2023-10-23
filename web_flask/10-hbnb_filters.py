#!/usr/bin/python3
"""script that starts a Flask web application"""

from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from flask import Flask, render_template
HostAddr = "0.0.0.0"
HostPort = 5000
app = Flask(__name__, template_folder="templates")


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """ """
    statesRAW = storage.all(State)
    citiesRAW = storage.all(City)
    amenitiesRAW = storage.all(Amenity)
    states = dict(sorted(
		statesRAW.items(), key=lambda item: item[1].name)
		)
    cities = dict(sorted(
		citiesRAW.items(), key=lambda item: item[1].name)
		)
    amenities = dict(sorted(
        amenitiesRAW.items(), key=lambda item: item[1].name)
        )
    return render_template(
        "10-hbnb_filters.html",
        states=states,
        cities=cities,
        amenities=amenities
        )


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
