from typing import List
from fastapi import APIRouter, Depends, status
from datamodels.schemas.verb import VerbBase, VerbInsert, VerbUpdate
from datamodels.cruds import verb
from sqlalchemy.orm import Session
from services.database import get_db
import logging


logger = logging.getLogger('router')
router = APIRouter(prefix='/verb', tags=['verb'])

@router.post(
    "/",
    response_model=VerbBase,
    summary="Create new Verb",
    status_code=status.HTTP_201_CREATED
)
async def add_verb(
    request: VerbInsert, 
    db: Session = Depends(get_db)):
    return verb.create(db=db, request=request)

@router.get("/all/",response_model=List[VerbBase])
async def get_all(db: Session = Depends(get_db)):
    """takes no args and returns all verbs."""

    return verb.get_all_verbs(db=db)


@router.patch("/update/id/{verb_id:int}/", response_model=VerbBase)
async def update_by_id(
    verb_id: int,
    request: VerbUpdate,
    db: Session = Depends(get_db)):
    return verb.update(
        db=db, request=request, verb_id=verb_id
    )


@router.delete("/delete/id/{verb_id:int}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(verb_id: int, db: Session = Depends(get_db)):
    """delete a verb by its id."""

    return verb.delete(db=db, verb_id=verb_id)
