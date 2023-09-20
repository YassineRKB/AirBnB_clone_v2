#!/usr/bin/python3
"""unitest Module: DB storage"""

# Model imports
from models import storage
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
# ALCHEMY
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

import inspect
import os
import unittest

env_value = os.environ.get("HBNB_TYPE_STORAGE")
known_classes = {
    "State": State,
    "City": City,
    "Place": Place,
    "Amenity": Amenity,
    "User": User,
    "Review": Review,
}

env = os.environ.get("HBNB_ENV")
user = os.environ.get("HBNB_MYSQL_USER")
pwd = os.environ.get("HBNB_MYSQL_PWD")
host = os.environ.get("HBNB_MYSQL_HOST")
database = os.environ.get("HBNB_MYSQL_DB")

DBStorage = None
if env_value == "db":
    DBStorage = db_storage.DBStorage


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db", "relevant")
class test_DBStorage(unittest.TestCase):
    """unitest class for db conn and operations"""

    def setUp(self):
        """new env"""
        try:
            self.engine = create_engine(
                "mysql+mysqldb://{}:{}@{}/{}".format(
                    user, pwd, host, database)
                ,pool_pre_ping=True,
            )
            self.Session = sessionmaker(bind=self.engine)
        except SQLAlchemyError as e:
            print(f"Failed: error connecting to the database: {e}")
        self.db_func = inspect.getmembers(DBStorage, inspect.isfunction)

    def tearDown(self):
        """Method to destroy storage file at the end of tests"""
        metadata = MetaData()
        session = self.Session()
        classes_to_delete = [Review, Amenity, Place, City, State, User]
        for cls in classes_to_delete:
            to_delete = session.query(cls).all()
            for item in to_delete:
                session.delete(item)
        session.commit()
        session.close()
        metadata.drop_all(self.engine, checkfirst=False)
        self.engine.dispose()

    def test_docstring(self):
        """unitest: DBStorage docstring"""
        if not DBStorage:
            return
        self.assertIsNot(DBStorage.__doc__, None)
        self.assertTrue(
            len(DBStorage.__doc__) >= 1,
            "DBStorage class needs a docstring"
        )

    def test_methods_docstrings(self):
        """unitest docstrings in DBStorage methods"""
        for func in self.db_func:
            self.assertIsNot(
                func[1].__doc__, None,
                "{:s} method is missing a docstring".format(func[0]),
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} method is missing a docstring".format(func[0]),
            )

    def test_module_docstring(self):
        """unitest db_storage.py module docstring"""
        self.assertIsNot(
            db_storage.__doc__, None,
            "db_storage.py is missing a docstring"
        )
        self.assertTrue(
            len(db_storage.__doc__) >= 1,
             "db_storage.py is missing a docstring"
        )

    def test_all(self):
        """unit test: return type"""
        session = self.Session()

        new_review = Review()
        new_user = User()
        new_city = City()
        new_state = State()
        new_amenity = Amenity()
        new_place = Place()

        new_review.place_id = new_place.id
        new_review.user_id = new_user.id
        new_review.text = "oz castle"

        new_amenity.name = "hellhounds"
        new_amenity.place_amenities.append(new_place)

        new_place.city_id = new_city.id
        new_place.user_id = new_user.id
        new_place.name = "mo"
        new_place.description = "sardinia's best inn"
        new_place.number_rooms = 50
        new_place.max_guest = 100
        new_place.price_by_night = 1000
        new_place.latitude = 11.0
        new_place.longitude = 15.5
        new_place.reviews.append(new_review)

        new_city.name = "Olympus"
        new_city.state_id = new_state.id
        new_city.places.append(new_place)

        new_state.name = "california"
        new_state.cities.append(new_city)

        new_user.email = "owner@amazon.com"
        new_user.password = "123password"
        new_user.first_name = "hackme"
        new_user.last_name = "pls"
        new_user.places.append(new_place)
        new_user.reviews.append(new_review)

        all_entries = [new_amenity, new_place, new_city, new_state, new_user]
        new_storage = storage
        new_storage.start_session()
        for i in all_entries:
            new_storage.new(i)
        new_storage.save()
        new_storage.stop_session()

        count = 0
        new_storage.start_session()
        all_cls = new_storage.all().values()
        for value in all_cls:
            for cls in known_classes.values():
                if isinstance(value, cls):
                    count += 1
        self.assertEqual(count, len(all_cls))
        new_storage.stop_session()
        session.close()

    def test_new(self):
        """test case for creation of newly created instances"""
        session = self.Session()

        new_review = Review()
        new_user = User()
        new_city = City()
        new_state = State()
        new_amenity = Amenity()
        new_place = Place()

        new_review.place_id = new_place.id
        new_review.user_id = new_user.id
        new_review.text = "hogwarts is better"

        new_amenity.name = "underground prison"
        new_amenity.place_amenities.append(new_place)

        new_place.city_id = new_city.id
        new_place.user_id = new_user.id
        new_place.name = "avalon"
        new_place.description = "the capital of magical uk"
        new_place.number_rooms = 4
        new_place.max_guest = 7
        new_place.price_by_night = 100
        new_place.latitude = 120.0
        new_place.longitude = 121.5
        new_place.reviews.append(new_review)

        new_city.name = "dullahan's castle"
        new_city.state_id = new_state.id
        new_city.places.append(new_place)

        new_state.name = "california"
        new_state.cities.append(new_city)

        new_user.email = "owner@amazon.com"
        new_user.password = "123password"
        new_user.first_name = "hackme"
        new_user.last_name = "pls"
        new_user.places.append(new_place)
        new_user.reviews.append(new_review)

        all_entries = [new_amenity, new_place, new_city, new_state, new_user]
        session.add_all(all_entries)
        session.commit()

        res_user = (
            session.query(User)
            .filter(
                User.first_name
                == "hackme\
"
            )
            .first()
        )

        self.assertIsNotNone(res_user)
        self.assertEqual(res_user.first_name, "hackme")
        self.assertIsNotNone(res_user.places)
        res_review = (
            session.query(Review)
            .filter(Review.text == "alaska looks pretty")
            .first()
        )
        self.assertEqual(res_review, new_review)
        session.close()

    def test_delete(self):
        """unit test: DBStorage delete action"""
        nStorage = storage
        nStorage.start_session()
        data = nStorage.all().values()
        for i in data:
            nStorage.delete(i)
        nStorage.save()
        data = nStorage.all().values()
        self.assertEqual(
            len(data), 0
        )
        nStorage.stop_session()

    def test_reload(self):
        """unit test: reload method"""
        new_storage = storage
        self.assertIsNotNone(new_storage.Session)
