from typing import List
from fastapi import APIRouter, Depends, status
from datamodels.schemas.quiz import QuizBase, QuizInsert, QuizUpdate
from datamodels.cruds import quiz
from sqlalchemy.orm import Session
from services.database import get_db
import logging


logger = logging.getLogger('router')
router = APIRouter(prefix='/quiz', tags=['quiz'])

@router.post(
    "/",
    response_model=QuizBase,
    summary="Create new Quiz",
    status_code=status.HTTP_201_CREATED
)
async def add_quiz(
    request: QuizInsert, 
    db: Session = Depends(get_db)):
    return quiz.create(db=db, request=request)

@router.get("/all/",response_model=List[QuizBase])
async def get_all(db: Session = Depends(get_db)):
    """takes no args and returns all quizs."""

    return quiz.get_all_quizs(db=db)


@router.patch("/update/id/{quiz_id:int}/", response_model=QuizBase)
async def update_by_id(
    quiz_id: int,
    request: QuizUpdate,
    db: Session = Depends(get_db)):
    return quiz.update(
        db=db, request=request, quiz_id=quiz_id
    )


@router.delete("/delete/id/{quiz_id:int}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(quiz_id: int, db: Session = Depends(get_db)):
    """delete a quiz by its id."""

    return quiz.delete(db=db, quiz_id=quiz_id)
