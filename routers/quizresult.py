from typing import List
from fastapi import APIRouter, Depends, status
from datamodels.schemas.quizresult import QuizResultBase, QuizResultInsert, QuizResultUpdate
from datamodels.cruds import quizresult
from sqlalchemy.orm import Session
from services.database import get_db
import logging


logger = logging.getLogger('router')
router = APIRouter(prefix='/quizresult', tags=['quizresult'])

@router.post(
    "/",
    response_model=QuizResultBase,
    summary="Create new QuizResult",
    status_code=status.HTTP_201_CREATED
)
async def add_quizresult(
    request: QuizResultInsert, 
    db: Session = Depends(get_db)):
    return quizresult.create(db=db, request=request)

@router.get("/all/",response_model=List[QuizResultBase])
async def get_all(db: Session = Depends(get_db)):
    """takes no args and returns all quizresults."""

    return quizresult.get_all_quizresults(db=db)


@router.patch("/update/id/{quizresult_id:int}/", response_model=QuizResultBase)
async def update_by_id(
    quizresult_id: int,
    request: QuizResultUpdate,
    db: Session = Depends(get_db)):
    return quizresult.update(
        db=db, request=request, quizresult_id=quizresult_id
    )


@router.delete("/delete/id/{quizresult_id:int}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(quizresult_id: int, db: Session = Depends(get_db)):
    """delete a quizresult by its id."""

    return quizresult.delete(db=db, quizresult_id=quizresult_id)
