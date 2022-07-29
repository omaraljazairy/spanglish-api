from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, status
from datamodels.schemas.word import (WordBase, WordInsert, WordUpdate,
                                     WordWithTranslationResponse, WordVerb)
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

@router.get("/all/",response_model=List[WordWithTranslationResponse])
async def get_all(db: Session = Depends(get_db)):
    """takes no args and returns all words."""

    return word.get_all_words(db=db)


@router.get("/id/{word_id:int}/",response_model=WordVerb)
async def get_word_by_id(word_id: int, db: Session = Depends(get_db)):
    """takes the word_id and returns a single word."""

    return word.get_word_by_id(db=db, word_id=word_id)


@router.get(
    "/category_id/{category_id:int}/",
    response_model=List[WordWithTranslationResponse])
async def get_by_category(
    category_id: int,
    limit: int = 100,
    offset: int = 0,
    exclude_from_result_date: datetime = None,
    db: Session = Depends(get_db)):
    """takes a category_id as a path parameter and limit, offset and the 
    exclude_from_result_date as query optional parameter.
    The exclude_from_result_date is optional and is only to exclude words 
    from that have been in the quizresult on that given date.
    """

    data = word.get_word_by_category(
        db=db,
        category_id=category_id,
        limit=limit,
        offset=offset,
        exclude_from_result_date=exclude_from_result_date)
    
    logger.debug(f"words found for category {category_id}: {data}")

    return data


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
