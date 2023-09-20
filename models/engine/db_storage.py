#!/usr/bin/python3
"""Module: DB implementing + alchemy orm"""
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
    """class for db implmentation"""

    Session = None
    __engine = None
    __session = None

    def __init__(self):
        """class constructor for db storage implementation"""
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, database),
            pool_pre_ping=True,
        )
        if env == "test":
            metadata = MetaData()
            metadata.drop_all(
                self.__engine, checkfirst=False
            )

    def all(self, cls=None):
        """method to return a dictionary
        of all queried class from the db"""
        from models.state import State, Base
        from models.city import City, Base
        from models.place import Place
        from models.amenity import Amenity
        from models.user import User
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

    def new(self, obj):
        """method to add new obj to current changes"""
        self.__session.add(obj)

    def save(self):
        """method save current changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """method to deletes an instance in database"""
        if obj:
            self.__session.delete(obj)

    def call(self, string):
        """method execute sql commands via engine"""
        self.__engine.execute(
            string
        )

    def start_session(self):
        """method to start a new session"""
        self.__session = DBStorage.Session()

    def stop_session(self):
        """method used to end a session"""
        self.save()
        self.__session.close()

    def reload(self):
        """method to init a thread-safe session"""
        from models.state import State, Base
        from models.city import City, Base
        from models.place import Place
        from models.amenity import Amenity
        from models.user import User
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        DBStorage.Session = scoped_session(
            sessionmaker(
                bind=self.__engine, expire_on_commit=False
            )
        )
        self.__session = DBStorage.Session()
