from datetime import datetime
from typing import Dict, List
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from datamodels.models import QuizQuestion, QuizResult, Word, Translation
from datamodels.schemas.word import WordInsert, WordUpdate
from exceptions.model_exceptions import AlreadyExistsException, NotFoundException
import logging

logger = logging.getLogger('crud')


def get_all_words(db: Session):
    """return all data from the word model."""

    return db.query(Word).all()


def get_word_by_category(
    db: Session, 
    category_id: int, 
    limit: int, 
    offset:int,
    exclude_from_result_date: datetime = None):
    """takes a category_id, limit, offset and an optional exclude_from_result_date
    and returns all words that belong to the category. If exclude_from_result_date
    is set with a date, it will exclude the words from the quizresult date."""

    if not exclude_from_result_date:
        # if not set, return all the words that belong to the category.

        return db.query(Word).filter(
            Word.category_id == category_id
            ).order_by(func.random()).offset(offset).limit(limit).all()

    else:
        # get the word_ids that need to be excluded
        used_words = db.query(
            QuizQuestion.word_id
            ).join(
                QuizResult, QuizResult.quizquestion_id == QuizQuestion.id
            ).filter(
                func.date(QuizResult.created) == func.date(exclude_from_result_date)
            ).all()

        # convert it to a set
        excluded_word_ids = {word_id['word_id'] for word_id in used_words}

        return db.query(Word).filter(
            Word.category_id == category_id
            ).filter(
                ~Word.id.in_(excluded_word_ids)
            ).order_by(
                func.random()
            ).offset(
                offset
            ).limit(
                limit
            ).all()

def get_word_by_id(db: Session, word_id: int) -> Dict:
    """takes the word_id as int and returns a dictionary of a single word 
    object.
    """

    word = db.query(Word).filter_by(id = word_id).first()
    return word


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
        text=request.text,
        category_id=request.category_id,
        translations=[
            Translation(
                language_id=translate.language_id,
                translation=translate.translation
            ) for translate in request.translations
        ]
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
