from fastapi import FastAPI, Depends
from src.core import models
from src.api.endpoints import auth, crud
from src.api.schemas import schemas
from src.dependencies.database import engine, SessionLocal
from sqlalchemy.orm import Session
from src.dependencies import dependencies
from fastapi.middleware.cors import CORSMiddleware
from src.authorization import get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
origins = [
    'http://localhost',
    'http://localhost:8180',
    'http://localhost:8190',
    'http://localhost:8200',
    'http://frontend:3000',
    'http://frontend:80',
    'http://reservation-web:8000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db), current_user: schemas.TokenData = Depends(get_current_user)):
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    return crud.get_user(db, user_id=user_id)

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(dependencies.get_db), current_user: schemas.TokenData = Depends(get_current_user)):
    return crud.update_user(db, user_id=user_id, user=user)

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(dependencies.get_db), current_user: schemas.TokenData = Depends(get_current_user)):
    return crud.delete_user(db, user_id=user_id)

@app.post("/token/", response_model=schemas.Token)
def generate_token(form_data: schemas.TokenRequest, db: Session = Depends(dependencies.get_db)):
    return auth.generate_token(db=db, form_data=form_data)

@app.post("/token/validate/", response_model=schemas.TokenData)
def validate_token(token: schemas.Token, db: Session = Depends(dependencies.get_db)):
    return auth.validate_token(db=db, token=token)