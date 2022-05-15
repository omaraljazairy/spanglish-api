from typing import List
from fastapi import APIRouter, Depends, status
from datamodels.schemas.translation import TranslationBase, TranslationInsert, TranslationUpdate
from datamodels.cruds import translation
from sqlalchemy.orm import Session
from services.database import get_db
import logging


logger = logging.getLogger('router')
router = APIRouter(prefix='/translation', tags=['translation'])

@router.post(
    "/",
    response_model=TranslationBase,
    summary="Create new Translation",
    status_code=status.HTTP_201_CREATED
)
async def add_translation(
    request: TranslationInsert, 
    db: Session = Depends(get_db)):
    return translation.create(db=db, request=request)

@router.get("/all/",response_model=List[TranslationBase])
async def get_all(db: Session = Depends(get_db)):
    """takes no args and returns all translations."""

    return translation.get_all_translations(db=db)


@router.patch("/update/id/{translation_id:int}/", response_model=TranslationBase)
async def update_by_id(
    translation_id: int,
    request: TranslationUpdate,
    db: Session = Depends(get_db)):
    return translation.update(
        db=db, request=request, translation_id=translation_id
    )


@router.delete("/delete/id/{translation_id:int}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(translation_id: int, db: Session = Depends(get_db)):
    """delete a translation by its id."""

    return translation.delete(db=db, translation_id=translation_id)
