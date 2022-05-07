from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Path
from datamodels.schemas import schema_auth, schema_income
from datamodels.cruds import crud_income
from sqlalchemy.orm import Session
# from sqlalchemy.sql.functions import current_user
from services.database import get_db
from app.config import get_settings, Settings
from routers import auth
import logging
from datetime import date


logger = logging.getLogger('router')
router = APIRouter(prefix='/income', tags=['income'])


@router.post("/", response_model=schema_income.Income)
async def add_income(
    income: schema_income.IncomeBase, 
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db),
    current_user: schema_auth.Login = Depends(auth.get_current_user)
    ):
    # get the customer_rate objct
    return crud_income.create(db=db, income=income)

    # return schema.taxed_income(income=income, settings=settings)


@router.get("/all/", response_model=List[schema_income.IncomeCustomResponse])
async def get_all_income(
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db),
    current_user: schema_auth.Login = Depends(auth.get_current_user)
    ):
    
    return crud_income.get_all_income(db=db)


@router.get(
    "/by_date/{start_date}/{end_date}/", 
    response_model=List[schema_income.IncomeCustomResponse])
async def get_by_invoice_date(
    start_date: date = Path(
        default=None,
        title="start_date of the invoice date",
        description="format: yyyy-mm-dd",
        example="2022-01-01"),
    end_date: date = Path(
        default=None,
        title="the last date of the invoice date",
        description="format: yyyy-mm-dd",
        example="2022-02-01"),
    db: Session = Depends(get_db),
    current_user: schema_auth.Login = Depends(auth.get_current_user)
    ):
    """
    Get all income data between two dates, start_date and end_date

    Args:
        start_date (date): This represents the invoice date. valid value yyyy-mm-dd
        end_date (date): This represents the invoice date. valid value yyyy-mm-dd

    Returns:
        json: list of all incomes between the start and end dates.
    """

    result = {'start_date': start_date, 'end_date': end_date }
    logger.debug(f"income params: {result}")

    return crud_income.get_income_by_date(db=db, start_date=start_date, end_date=end_date)


@router.get(
    "/by_customer/{customer_id}/", 
    response_model=List[schema_income.IncomeCustomResponse])
async def get_by_customer_id(
    customer_id:int,
    db: Session = Depends(get_db),
    current_user: schema_auth.Login = Depends(auth.get_current_user)
    ):

    return crud_income.get_income_by_customer(db=db, customer_id=customer_id)
    