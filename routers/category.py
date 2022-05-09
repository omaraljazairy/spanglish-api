from typing import List
from fastapi import APIRouter, Depends, status
from datamodels.schemas.category import CategoryBase, CategoryInsertUpdate
from datamodels.cruds import category
from sqlalchemy.orm import Session
from services.database import get_db
import logging


logger = logging.getLogger('router')
router = APIRouter(prefix='/category', tags=['category'])

@router.post(
    "/",
    response_model=CategoryBase,
    summary="Create new Category",
    status_code=status.HTTP_201_CREATED
)
async def add_category(
    request: CategoryInsertUpdate, 
    db: Session = Depends(get_db)):
    return category.create(db=db, request=request)

@router.get("/all/",response_model=List[CategoryBase])
async def get_all(db: Session = Depends(get_db)):
    """takes no args and returns all categorys."""

    return category.get_all_categorys(db=db)


@router.patch("/update/id/{category_id:int}/", response_model=CategoryBase)
async def update_by_id(
    category_id: int,
    request: CategoryInsertUpdate,
    db: Session = Depends(get_db)):
    return category.update(
        db=db, request=request, category_id=category_id
    )


@router.delete("/delete/id/{category_id:int}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(category_id: int, db: Session = Depends(get_db)):
    """delete a category by its id."""

    return category.delete(db=db, category_id=category_id)
