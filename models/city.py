#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
import os
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

envDB = os.environ.get("HBNB_TYPE_STORAGE")


class City(BaseModel, Base):
    """The city class, contains state ID and name"""

    __tablename__ = "cities"
    if envDB == "db":
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="cities")
        state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    else:
        state_id = ""
        name = ""
