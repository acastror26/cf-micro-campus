from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from jose.exceptions import JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.api.endpoints import crud
from src.api.schemas import schemas
from src.dependencies.dependencies import get_db

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 360 # 6 hours

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(db: Session, email: str, password: str):
    user = crud.get_user_by_email(db, email=email)
    if not user:
        return False
    if not crud.verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_token(db: Session, form_data: schemas.TokenRequest):
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "is_active": user.is_active}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer", expires_in=ACCESS_TOKEN_EXPIRE_MINUTES)

def validate_token(db: Session, token: schemas.Token):
    def credentials_exception(detail=''):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials. Detail: " + detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception(detail='email is None. Payload: ' + str(payload))
    except JWTError:
        raise credentials_exception(detail='JWTError. Token: ' + token.access_token)
    user = crud.get_user_by_email(db, email=email)
    token_data = schemas.TokenData(user=user, is_valid=True)
    if user is None:
        raise credentials_exception(detail='user not found')
    return token_data
