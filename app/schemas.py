"""Schema for the database models."""
# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=too-few-public-methods
from typing import Optional
from pydantic import BaseModel


class SentenceBase(BaseModel):
    """Base model for the sentence.

    :param BaseModel: Base model
    :type BaseModel: BaseModel
    """
    sentence: str
    labeled: Optional[int] = 3


class Sentence(SentenceBase):
    """Sentence model.

    :param SentenceBase: Base model
    :type SentenceBase: SentenceBase
    """
    id: int

    class Config:
        """Config for the model.
        """
        orm_mode = True
