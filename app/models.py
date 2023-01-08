"""Models for the database."""
# pylint: disable=too-few-public-methods
from sqlalchemy import Column, Integer, String

from .database import Base


class Sentences(Base):
    """Sentences model.

    :param Base: Base model
    :type Base: Base
    """
    __tablename__ = "sentences"
    id = Column(Integer, primary_key=True, index=True)
    sentence = Column(String)
    labeled = Column(Integer, default=3)
