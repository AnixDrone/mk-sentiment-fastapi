"""Main app module."""
import time
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

from fastapi import Depends, FastAPI, HTTPException

from . import crud
from . import models
from . import schemas
from .database import SessionLocal, engine


for i in range(10):
    try:
        models.Base.metadata.create_all(bind=engine)
        break
    except OperationalError:
        time.sleep(i + 1)


app = FastAPI()


def get_db():
    """Get database session.

    :yield: Database session
    :rtype: Session
    """
    data_base = SessionLocal()
    try:
        yield data_base
    finally:
        data_base.close()


@app.get("/sentence", response_model=schemas.Sentence)
def get_unlabeled_sentece(
    data_base: Session = Depends(get_db)
):
    """Get unlabeled sentence.

    :param data_base: Database, defaults to Depends(get_db)
    :type data_base: Session, optional
    :return: Sentence
    :rtype: schemas.Sentence
    """
    sentence = crud.get_unlabeled_sentece(data_base)
    return sentence


@app.get("/random_sentence", response_model=schemas.Sentence)
def get_random_sentence(
    data_base: Session = Depends(get_db)
):
    """Get random sentence.

    :param data_base: Data base, defaults to Depends(get_db)
    :type data_base: Session, optional
    :return: Sentence
    :rtype: schemas.Sentence
    """
    sentence = crud.get_random_sentence(data_base)
    return sentence


@app.get("/sentence/{sentence_id}", response_model=schemas.Sentence)
def get_sentence(sentence_id: int, data_base: Session = Depends(get_db)):
    """Get sentence by id."""
    return crud.get_sentence(data_base, sentence_id)


@app.post("/sentence", response_model=schemas.Sentence)
def create_sentence(sentence: schemas.SentenceBase, data_base: Session = Depends(get_db)):
    """Create sentence.

    :param sentence: Sentence
    :type sentence: schemas.SentenceBase
    :param data_base: DataBase, defaults to Depends(get_db)
    :type data_base: Session, optional
    :raises HTTPException: Sentence already exist
    :return: Sentence
    :rtype: schemas.Sentence
    """
    db_sentence = crud.get_sentence_by_sentence(data_base, sentence.sentence)
    if db_sentence is not None:
        raise HTTPException(status_code=400, detail="Sentence already exist")
    return crud.create_sentece(data_base=data_base, sentence_base=sentence)


@app.get("/sentence/{sentence_id}/{label}", response_model=schemas.Sentence)
def label_sentence(sentence_id: int, label: int, data_base: Session = Depends(get_db)):
    """Label sentence.

    :param sentence_id: _description_
    :type sentence_id: int
    :param label: The label of the sentence
    :type label: int
    :param data_base: Database, defaults to Depends(get_db)
    :type data_base: Session, optional
    :return: Sentence
    :rtype: schemas.Sentence
    """
    db_sentence = crud.label_sentence(
        data_base=data_base, sentence_id=sentence_id, label=label)
    return db_sentence
