from turtle import title
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
# from datamodels.schema import Customer, CustomerBase, CustomerResponse, CustomerUpdate
from datamodels import models
from datamodels.schemas import schema_auth, schema_customer
from datamodels.cruds import crud_customer
from sqlalchemy.orm import Session
from app.config import get_settings, Settings
# from sqlalchemy.sql.functions import current_user
from services.database import get_db
from routers import auth
import logging


logger = logging.getLogger('router')
router = APIRouter(prefix='/customer', tags=['customer'])


@router.post(
    "/",
    response_model=schema_customer.CustomerResponse,
    summary="Create new customer",
    status_code=status.HTTP_201_CREATED
)
async def add_customer(
    customer: schema_customer.CustomerBase, 
    db: Session = Depends(get_db)):
    existing_customer = db.query(models.Customer).filter(
        models.Customer.name == customer.name
        ).first()
    logger.info(f"existing_customer => {existing_customer}")
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Customer {customer.name} already exists"
        )
    return crud_customer.create(db=db, customer=customer)


@router.get(
    "/all", 
    response_model=List[schema_customer.CustomerResponse], 
    summary="Get all customers",
    status_code=status.HTTP_200_OK
)
async def get_all_customers(
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db),
    current_user: schema_auth.Login = Depends(auth.get_current_user)
    ):
    """
    Returns all Customers.
    """
    return crud_customer.get_all_customers(db=db)


@router.get(
    "/{customer_id}", 
    response_model=schema_customer.CustomerDetailResponse, 
    summary="Get customer by customer_id",
    status_code=status.HTTP_200_OK
)
async def get_all_customers(
    customer_id: int,
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db),
    current_user: schema_auth.Login = Depends(auth.get_current_user)
    ):
    """
    Returns one customer
    - **customer_id** mandatory path parameter
    """
    
    return crud_customer.get_customer_by_id(db=db, id=customer_id)


# update customer
@router.put(
    "/update/", 
    response_model=schema_customer.Customer, 
    summary="Update existing customer"
    )
async def update_customer(
    customer: schema_customer.CustomerUpdate, 
    db: Session = Depends(get_db
    )):
    """
    update a single customer name by providing the customer_id and name in 
    the json body.
    - **id** body parameter of an existing customer
    - **name** body parameter
    """
    # check if customer exists first, else, return an http error NOT FOUND
    existing_customer = db.query(models.Customer).get(customer.id)
    logger.info(f"customer: {customer} is {existing_customer}")
    if not existing_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id {customer.id} does not exist"
        )
    return crud_customer.update(db=db, customer=customer)


@router.delete(
    "/delete/customer_id/{customer_id:int}/", 
    status_code=204, 
    summary="Delete existing customer"
    )
async def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    # check if customer exists first, else, return an http error NOT FOUND
    existing_customer = db.query(models.Customer).get(customer_id)
    logger.info(f"customer with id: {customer_id} is {existing_customer}")
    if not existing_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with id {customer_id} does not exist"
        )
    crud_customer.delete(db=db, customer_id=customer_id)
