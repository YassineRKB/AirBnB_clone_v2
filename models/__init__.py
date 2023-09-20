#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.user import User
from models.review import Review
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from os import environ


storage_engine = environ.get("HBNB_TYPE_STORAGE")

storage = DBStorage() if storage_engine == "db" else FileStorage()
storage.reload()
