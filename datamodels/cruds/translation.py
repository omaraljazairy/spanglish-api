from sqlalchemy.orm import Session
from datamodels.models import Translation
from datamodels.schemas.translation import TranslationInsert, TranslationUpdate
from exceptions.model_exceptions import AlreadyExistsException, NotFoundException
import logging

logger = logging.getLogger('crud')


def get_all_translations(db: Session):
    """return all data from the translation model."""

    return db.query(Translation).all()


def create(db: Session, request: TranslationInsert):
    """create a new Translation object. check first if the records doesn't exist."""

    existing_translation = db.query(Translation).filter(
    Translation.word_id == request.word_id
    ).first()
    
    if existing_translation:
        logger.error(f"existing_translation => {existing_translation}")
        raise AlreadyExistsException(
            msg=f"Translation for word_id {request.word_id} already exists"
        )

    db_translation = Translation(
        **request.dict()
    )
    db.add(db_translation)
    db.commit()
    db.refresh(db_translation)
    return db_translation


def update(db: Session, request: TranslationUpdate, translation_id: int):
    """
    update the translation model. take the TranslationUpdate schema and a 
    translation_id as params. returns a translation object.
    """
    db_translation = db.query(Translation).get(translation_id)
    # throw an exception if not found
    if not db_translation:
        raise NotFoundException(
            msg=f"translation with id {translation_id} is not found"
        )
    
    requested_translation = request.dict(exclude_unset=True)
    for key, value in requested_translation.items():
        setattr(db_translation, key, value)
    db.add(db_translation)
    db.commit()
    db.refresh(db_translation)
    return db_translation


def delete(db: Session, translation_id: int ) -> None:
    """delete the translation object if found, else raise an exception."""

    db_translation = db.query(Translation).get(translation_id)
    # throw an exception if not found
    if not db_translation:
        raise NotFoundException(
            msg=f"translation with id {translation_id} doesn't exist"
        )
    db.delete(db_translation)
    db.commit()
