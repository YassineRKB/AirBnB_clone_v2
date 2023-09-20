#!/usr/bin/python3
""" Review module for the HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

envDB = os.environ.get("HBNB_TYPE_STORAGE")


class Review(BaseModel, Base):
    """Review classto store review information"""

    __tablename__ = "reviews"
    if envDB != "db":
        place_id = ""
        user_id = ""
        text = ""
    else:
        text = Column(String(1024), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
