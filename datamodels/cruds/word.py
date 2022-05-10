from sqlalchemy.orm import Session
from datamodels.models import Word
from datamodels.schemas.word import WordInsert, WordUpdate
from exceptions.model_exceptions import AlreadyExistsException, NotFoundException
import logging

logger = logging.getLogger('crud')


def get_all_words(db: Session):
    """return all data from the word model."""

    return db.query(Word).all()


def create(db: Session, request: WordInsert):
    """create a new Word object. check first if the records doesn't exist."""

    existing_word = db.query(Word).filter(
    Word.word == request.word
    ).first()
    
    if existing_word:
        logger.error(f"existing_word => {existing_word}")
        raise AlreadyExistsException(
            msg=f"Word {request.word} already exists"
        )

    db_word = Word(
        **request.dict()
    )
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word


def update(db: Session, request: WordUpdate, word_id: int):
    """
    update the word model. take the WordUpdate schema and a 
    word_id as params. returns a word object.
    """
    word_db = db.query(Word).get(word_id)
    # throw an exception if not found
    if not word_db:
        raise NotFoundException(
            msg=f"word with id {word_id} is not found"
        )
    
    requested_word = request.dict(exclude_unset=True)
    for key, value in requested_word.items():
        setattr(word_db, key, value)
    db.add(word_db)
    db.commit()
    db.refresh(word_db)
    return word_db


def delete(db: Session, word_id: int ) -> None:
    """delete the word object if found, else raise an exception."""

    word_db = db.query(Word).get(word_id)
    # throw an exception if not found
    if not word_db:
        raise NotFoundException(
            msg=f"word with id {word_id} doesn't exist"
        )
    db.delete(word_db)
    db.commit()
