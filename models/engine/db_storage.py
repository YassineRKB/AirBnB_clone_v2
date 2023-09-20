#!/usr/bin/python3
"""a module that defines the database storage implementation"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import MetaData
import os

user = os.environ.get("HBNB_MYSQL_USER")
pwd = os.environ.get("HBNB_MYSQL_PWD")
host = os.environ.get("HBNB_MYSQL_HOST")
database = os.environ.get("HBNB_MYSQL_DB")
env = os.environ.get("HBNB_ENV")


class DBStorage:
    """An implementation of the Database Storage"""

    __engine = None
    __session = None
    Session = None

    def __init__(self):
        """init"""
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, database),
            pool_pre_ping=True,
        )
        if env == "test":
            metadata = MetaData()
            metadata.drop_all(self.__engine, checkfirst=False)

    def all(self, cls=None):
        """method to list all instances"""
        from models.amenity import Amenity
        from models.user import User
        from models.place import Place
        from models.state import State, Base
        from models.city import City, Base
        from models.review import Review

        if cls is None:
            cls = [State, City, User, Place, Review, Amenity]
            query = []
            for c in cls:
                query.extend(self.__session.query(c).all())
        else:
            query = self.__session.query(cls).all()
        cls_objs = {}
        for obj in query:
            cls_objs[obj.to_dict()["__class__"] + "." + obj.id] = obj
        return cls_objs

    def reload(self):
        """method to create database session"""
        from models.user import User
        from models.amenity import Amenity
        from models.place import Place
        from models.state import State, Base
        from models.city import City, Base
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        DBStorage.Session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False)
        )
        self.__session = DBStorage.Session()

    def new(self, obj):
        """method to add new obj to session"""
        self.__session.add(obj)

    def delete(self, obj=None):
        """method to del obj from current session"""
        if obj:
            self.__session.delete(obj)

    def save(self):
        """method to save current session operations"""
        self.__session.commit()

    def call(self, string):
        """method to execute sql cmd"""
        self.__engine.execute(string)

    def start_session(self):
        """method to start new session"""
        self.__session = DBStorage.Session()

    def stop_session(self):
        """method to end current session"""
        self.save()
        self.__session.close()

