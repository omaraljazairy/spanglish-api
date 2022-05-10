from typing import List
from fastapi import APIRouter, Depends, status
from datamodels.schemas.word import WordBase, WordInsert, WordUpdate
from datamodels.cruds import word
from sqlalchemy.orm import Session
from services.database import get_db
import logging


logger = logging.getLogger('router')
router = APIRouter(prefix='/word', tags=['word'])

@router.post(
    "/",
    response_model=WordBase,
    summary="Create new Word",
    status_code=status.HTTP_201_CREATED
)
async def add_word(
    request: WordInsert, 
    db: Session = Depends(get_db)):
    return word.create(db=db, request=request)

@router.get("/all/",response_model=List[WordBase])
async def get_all(db: Session = Depends(get_db)):
    """takes no args and returns all words."""

    return word.get_all_words(db=db)


@router.patch("/update/id/{word_id:int}/", response_model=WordBase)
async def update_by_id(
    word_id: int,
    request: WordUpdate,
    db: Session = Depends(get_db)):
    return word.update(
        db=db, request=request, word_id=word_id
    )


@router.delete("/delete/id/{word_id:int}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(word_id: int, db: Session = Depends(get_db)):
    """delete a word by its id."""

    return word.delete(db=db, word_id=word_id)
