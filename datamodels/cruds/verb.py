from sqlalchemy.orm import Session
from datamodels.models import Verb, Word
from datamodels.schemas.verb import VerbInsert, VerbUpdate
from exceptions.model_exceptions import ( AlreadyExistsException,
    NotFoundException, WordNotVerbException)
import logging

logger = logging.getLogger('crud')


def get_all_verbs(db: Session):
    """return all data from the verb model."""

    return db.query(Verb).all()


def create(db: Session, request: VerbInsert):
    """
    create a new Verb object. check first if the record doesn't exist
    and the category name is verb.
    """

    existing_verb = db.query(Verb).filter(
    Verb.word_id == request.word_id
    ).first()
    
    if existing_verb:
        logger.error(f"existing_verb => {existing_verb}")
        raise AlreadyExistsException(
            msg=f"Verb from the word_id {request.word_id} already exists"
        )
    # get the category of the word and check if it is Verb, otherwise
    # raise a WordNotVerbException exception.
    word = db.query(Word).get(request.word_id)
    if word.category_name != 'Verb':
        raise WordNotVerbException(
            msg=f"The Category of the word {word.id} is not Verb"
        )

    db_verb = Verb(
        **request.dict()
    )
    db.add(db_verb)
    db.commit()
    db.refresh(db_verb)
    return db_verb


def update(db: Session, request: VerbUpdate, verb_id: int):
    """
    update the verb model. take the VerbUpdate schema and a 
    verb_id as params. returns a Verb object.
    """
    db_verb = db.query(Verb).get(verb_id)
    # throw an exception if not found
    if not db_verb:
        raise NotFoundException(
            msg=f"verb with id {verb_id} is not found"
        )
    
    requested_word = request.dict(exclude_unset=True)
    for key, value in requested_word.items():
        setattr(db_verb, key, value)
    db.add(db_verb)
    db.commit()
    db.refresh(db_verb)
    return db_verb


def delete(db: Session, verb_id: int ) -> None:
    """delete the verb object if found, else raise an exception."""

    db_verb = db.query(Verb).get(verb_id)
    # throw an exception if not found
    if not db_verb:
        raise NotFoundException(
            msg=f"verb with id {verb_id} doesn't exist"
        )
    db.delete(db_verb)
    db.commit()
