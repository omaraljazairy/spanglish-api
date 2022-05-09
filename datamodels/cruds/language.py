from sqlalchemy.orm import Session
from datamodels.models import Language
from datamodels.schemas.language import LanguageInsert, LanguageUpdate
from exceptions.model_exceptions import AlreadyExistsException, NotFoundException
import logging

logger = logging.getLogger('crud')


def get_all_languages(db: Session):
    """return all data from the language model."""

    return db.query(Language).all()


def create(db: Session, request: LanguageInsert):
    """create a new Language object. check first if the records doesn't exist."""

    existing_language = db.query(Language).filter(
    Language.code == request.code
    ).first()
    
    if existing_language:
        logger.error(f"existing_language => {existing_language}")
        raise AlreadyExistsException(
            msg=f"Language {request.code} already exists"
        )

    db_language = Language(
        **request.dict()
    )
    db.add(db_language)
    db.commit()
    db.refresh(db_language)
    return db_language


def update(db: Session, request: LanguageUpdate, language_id: int):
    """
    update the language model. take the LanguageUpdate schema and a 
    language_id as params. returns a language object.
    """
    language_db = db.query(Language).get(language_id)
    # throw an exception if not found
    if not language_db:
        raise NotFoundException(
            msg=f"language with id {language_id} is not found"
        )
    
    requested_language = request.dict(exclude_unset=True)
    for key, value in requested_language.items():
        setattr(language_db, key, value)
    db.add(language_db)
    db.commit()
    db.refresh(language_db)
    return language_db


def delete(db: Session, language_id: int ) -> None:
    """delete the language object if found, else raise an exception."""

    language_db = db.query(Language).get(language_id)
    # throw an exception if not found
    if not language_db:
        raise NotFoundException(
            msg=f"language with id {language_id} doesn't exist"
        )

    db.delete(language_db)
    db.commit()
