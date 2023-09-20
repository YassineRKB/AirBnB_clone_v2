#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
import os

var = "HBNB_TYPE_STORAGE"
env_value = os.environ.get(var)

if env_value != "db":
    from models.engine.file_storage import FileStorage

    storage = FileStorage()
else:
    from models.engine.db_storage import DBStorage

    storage = DBStorage()
storage.reload()
