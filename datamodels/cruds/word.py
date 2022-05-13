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
    Word.text == request.text
    ).first()
    
    if existing_word:
        logger.error(f"existing_word => {existing_word}")
        raise AlreadyExistsException(
            msg=f"Word {request.text} already exists"
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
    db_word = db.query(Word).get(word_id)
    # throw an exception if not found
    if not db_word:
        raise NotFoundException(
            msg=f"word with id {word_id} is not found"
        )
    
    requested_word = request.dict(exclude_unset=True)
    for key, value in requested_word.items():
        setattr(db_word, key, value)
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word


def delete(db: Session, word_id: int ) -> None:
    """delete the word object if found, else raise an exception."""

    db_word = db.query(Word).get(word_id)
    # throw an exception if not found
    if not db_word:
        raise NotFoundException(
            msg=f"word with id {word_id} doesn't exist"
        )
    db.delete(db_word)
    db.commit()
