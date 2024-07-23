from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.dependencies import dependencies
from src.api.schemas import schemas
from src.api.endpoints import auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Security(oauth2_scheme), db: Session = Depends(dependencies.get_db)):
    token_data = auth.validate_token(db=db, token=schemas.Token(access_token=token, token_type="bearer"))
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token_data