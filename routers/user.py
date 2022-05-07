from fastapi import APIRouter, Depends
from datamodels import models
from datamodels.schemas import schema_auth
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from services.database import get_db

router = APIRouter(prefix='/user', tags=['user'])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/')
def create(request: schema_auth.UserBase, db: Session = Depends(get_db)):
    hashed_pwd = pwd_context.hash(request.password)
    request.password = hashed_pwd
    db_user = models.User(**request.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

