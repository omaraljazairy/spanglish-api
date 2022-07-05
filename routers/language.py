from typing import List
from fastapi import APIRouter, Depends, status
from datamodels.schemas.language import LanguageBase, LanguageInsert, LanguageUpdate
from datamodels.cruds import language
from sqlalchemy.orm import Session
from services.database import get_db
import logging


logger = logging.getLogger('router')
router = APIRouter(prefix='/language', tags=['language'])

@router.post(
    "/",
    response_model=LanguageBase,
    summary="Create new Language",
    status_code=status.HTTP_201_CREATED
)
async def add_language(
    request: LanguageInsert, 
    db: Session = Depends(get_db)):

    return language.create(db=db, request=request)

@router.get("/all/",response_model=List[LanguageBase])
async def get_all(db: Session = Depends(get_db)):
    """takes no args and returns all languages."""

    return language.get_all_languages(db=db)


@router.patch("/update/id/{language_id:int}/", response_model=LanguageBase)
async def update_by_id(
    language_id: int,
    request: LanguageUpdate,
    db: Session = Depends(get_db)):
    return language.update(
        db=db, request=request, language_id=language_id
    )


@router.delete("/delete/id/{language_id:int}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(language_id: int, db: Session = Depends(get_db)):
    """delete a language by its id."""

    return language.delete(db=db, language_id=language_id)
