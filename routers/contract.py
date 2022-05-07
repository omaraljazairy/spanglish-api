from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from datamodels.schemas import schema_contract
from datamodels import models
from datamodels.cruds import crud_contract
from sqlalchemy.orm import Session
# from sqlalchemy.sql.functions import current_user
from services.database import get_db
# from routers import auth
import logging


logger = logging.getLogger('router')
router = APIRouter(prefix='/contract', tags=['contract'])


@router.post("/", response_model=schema_contract.ContractResponse)
async def add_contract(
    contract: schema_contract.ContractBase, 
    db: Session = Depends(get_db)):
    existing_customer = db.query(models.Customer).filter(
        models.Customer.id == contract.customer_id
        ).first()
    logger.info(f"existing_customer => {existing_customer}")
    if not existing_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer does not exist"
        )
    return crud_contract.create(db=db, contract=contract)


@router.patch(
    "/update/contract_id/{contract_id:int}/",
    response_model=schema_contract.ContractResponse)
async def update_contract(
    contract_id: int,
    contract: schema_contract.ContractUpdate,
    db: Session = Depends(get_db)
    ):
    """takes the contract_id and a ContractUpdate model in the body of the request, 
    checks first if the contract exists, update it and return 200. 
    else a 400 http error.
    """
    existing_contract = db.query(models.Contract).get(contract_id)
    logger.info(f"existing_contract => {existing_contract}")
    if not existing_contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contract does not exist"
        )
    return crud_contract.update(db=db, contract=contract, id=contract_id)

@router.delete("/delete/contract_id/{contract_id:int}/", status_code=204, summary="Delete existing customer")
async def delete_contract(contract_id: int, db: Session = Depends(get_db)):
    # check if contract exists first, else, return an http error NOT FOUND
    existing_contract = db.query(models.Contract).get(contract_id)
    logger.info(f"contract with id: {contract_id} is {existing_contract}")
    if not existing_contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contract with id {id} does not exist"
        )
    crud_contract.delete(db=db, contract_id=contract_id)


@router.get("/all/", response_model=List[schema_contract.ContractResponse])
async def get_all(db: Session = Depends(get_db)):
    """Takes no params and returns a list of contracts."""

    return crud_contract.fetch_all(db = db)


@router.get(
    "/contract_id/{contract_id:int}/", 
    response_model=schema_contract.ContractDetails)
async def get_all(contract_id: int, db: Session = Depends(get_db)):
    """Takes a contract_id int and returns the contract details response."""

    return crud_contract.fetch_by_id(contract_id=contract_id, db=db)
