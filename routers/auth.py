from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from datamodels import models
from datamodels.schemas import schema_auth
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from services.database import get_db
import logging
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY_TEMP = 'asecretkey1234'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60

logger = logging.getLogger('router')

router = APIRouter(prefix='/auth', tags=['auth'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def generate_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_TEMP, algorithm=ALGORITHM)

    return encoded_jwt
    

@router.post('/login')
# def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
def login(request: schema_auth.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    logger.info(f"user => {user}")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
            )
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Incorrect password'
            )
    access_token = generate_token(
        data={"sub": user.username}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):

    # credential exception
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid credentials",
        headers={'WWW-Authenticate': "Bearer"}
    )


    try:
        payload = jwt.decode(token, SECRET_KEY_TEMP, algorithms=[ALGORITHM])
        logger.info(f"payload received: => {payload}")
        username = payload.get('sub')
        if not username:
            logger.info("no username available")
            raise credential_exception
        token_data = schema_auth.TokenData(username=username)
        logger.info(f"token_data => {token_data}")
    except JWTError as e:
        logger.error(f"{e}")
        raise credential_exception
        


