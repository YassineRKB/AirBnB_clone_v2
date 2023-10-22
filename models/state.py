#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import os

envDB = os.environ.get("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    """State class"""
    __tablename__ = "states"
    if envDB == "db":
        name = Column(String(128), nullable=False)
        cities = relationship(
            "City", backref="state"
        )
    else:
        name = ""

        @property
        def cities(self):
            from models.__init__ import storage
            from models.city import City

            obj_list = []
            strg = storage.all(City)
            for value in strg.items():
                if self.id == value.state_id:
                    obj_list.append(value)
            return obj_list
