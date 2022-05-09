from sqlalchemy.orm import Session
from datamodels.models import Category
from datamodels.schemas.category import CategoryInsertUpdate
from exceptions.model_exceptions import AlreadyExistsException, NotFoundException
import logging

logger = logging.getLogger('crud')


def get_all_categorys(db: Session):
    """return all data from the category model."""

    return db.query(Category).all()


def create(db: Session, request: CategoryInsertUpdate):
    """create a new Category object. check first if the records doesn't exist."""

    existing_category = db.query(Category).filter(
        Category.name == request.name).first()
    
    if existing_category:
        logger.error(f"category {request.name} already exists")
        raise AlreadyExistsException(
            msg=f"Category {request.name} already exists"
        )

    db_category = Category(
        **request.dict()
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update(db: Session, request: CategoryInsertUpdate, category_id: int):
    """
    update the category model. take the CategoryInsertUpdate schema and a 
    category_id as params. returns a category object.
    """
    category_db = db.query(Category).get(category_id)
    # throw an exception if not found
    if not category_db:
        raise NotFoundException(
            msg=f"category with id {category_id} is not found"
        )
    
    requested_category = request.dict(exclude_unset=True)
    for key, value in requested_category.items():
        setattr(category_db, key, value)
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return category_db


def delete(db: Session, category_id: int ) -> None:
    """delete the category object if found, else raise an exception."""

    category_db = db.query(Category).get(category_id)
    # throw an exception if not found
    if not category_db:
        raise NotFoundException(
            msg=f"category with id {category_id} doesn't exist"
        )

    db.delete(category_db)
    db.commit()
