"""CRUD operations."""
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from . import models
from . import schemas


def get_sentence(data_base: Session, sentence_id: int):
    """Get sentence by id.

    :param data_base: Database session
    :type data_base: Session
    :param sentence_id: Sentence id
    :type sentence_id: int
    :return: Sentence
    :rtype: models.Sentences
    """
    return data_base.query(models.Sentences).filter(models.Sentences.id == sentence_id).first()


def get_random_sentence(data_base: Session):
    """Get random sentence.

    :param data_base: Database session
    :type data_base: Session
    :return: Sentence
    :rtype: models.Sentences
    """
    return data_base.query(models.Sentences)\
        .order_by(func.random())\
        .filter(models.Sentences.labeled == 3)\
        .first()


def get_unlabeled_sentece(data_base: Session):
    """Get unlabeled sentence.

    :param data_base: Database session
    :type data_base: Session
    :return: Sentence
    :rtype: models.Sentences
    """
    return data_base.query(models.Sentences).filter(models.Sentences.labeled == 3).first()


def get_sentence_by_sentence(data_base: Session, sentence: str):
    """Get sentence by sentence.

    :param data_base: Database session
    :type data_base: Session
    :param sentence: Sentence
    :type sentence: str
    :return: Sentence
    :rtype: models.Sentences
    """
    return data_base.query(models.Sentences).filter(models.Sentences.sentence == sentence).first()


def create_sentece(data_base: Session, sentence_base: schemas.SentenceBase):
    """Create sentence.

    :param data_base: Database session
    :type data_base: Session
    :param sentence_base: Sentence
    :type sentence_base: schemas.SentenceBase
    :return: Sentence
    :rtype: schemas.Sentence
    """
    db_sentence = models.Sentences(sentence=sentence_base.sentence)
    data_base.add(db_sentence)
    data_base.commit()
    data_base.refresh(db_sentence)
    return schemas.Sentence(id=db_sentence.id,
                            sentence=db_sentence.sentence,
                            labeled=db_sentence.labeled)


def label_sentence(data_base: Session, sentence_id: int, label: int):
    """Label sentence.

    :param data_base: Database session
    :type data_base: Session
    :param sentence_id: Sentence id
    :type sentence_id: int
    :param label: Label
    :type label: int
    :return: Sentence
    :rtype: models.Sentences
    """
    db_sentence = data_base.query(models.Sentences).filter(
        models.Sentences.id == sentence_id).first()
    db_sentence.labeled = label
    data_base.commit()
    data_base.refresh(db_sentence)
    return db_sentence
