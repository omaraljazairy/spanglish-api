from typing import List
from fastapi import APIRouter, Depends, status
from datamodels.schemas.quizquestion import QuizQuestionBase, QuizQuestionInsert, QuizQuestionUpdate
from datamodels.cruds import quizquestion
from sqlalchemy.orm import Session
from services.database import get_db
import logging


logger = logging.getLogger('router')
router = APIRouter(prefix='/quizquestion', tags=['quizquestion'])

@router.post(
    "/",
    response_model=QuizQuestionBase,
    summary="Create new QuizQuestion",
    status_code=status.HTTP_201_CREATED
)
async def add_quizquestion(
    request: QuizQuestionInsert, 
    db: Session = Depends(get_db)):
    return quizquestion.create(db=db, request=request)

@router.get("/all/",response_model=List[QuizQuestionBase])
async def get_all(db: Session = Depends(get_db)):
    """takes no args and returns all quizquestions."""

    return quizquestion.get_all_quizquestions(db=db)


@router.patch("/update/id/{quizquestion_id:int}/", response_model=QuizQuestionBase)
async def update_by_id(
    quizquestion_id: int,
    request: QuizQuestionUpdate,
    db: Session = Depends(get_db)):
    return quizquestion.update(
        db=db, request=request, quizquestion_id=quizquestion_id
    )


@router.delete("/delete/id/{quizquestion_id:int}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(quizquestion_id: int, db: Session = Depends(get_db)):
    """delete a quizquestion by its id."""

    return quizquestion.delete(db=db, quizquestion_id=quizquestion_id)
