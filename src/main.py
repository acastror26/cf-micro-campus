from fastapi import FastAPI, Depends
from src import models, schemas, crud, auth, dependencies
from src.database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    return crud.get_user(db, user_id=user_id)

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(dependencies.get_db)):
    return crud.update_user(db, user_id=user_id, user=user)

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    return crud.delete_user(db, user_id=user_id)

@app.post("/token/", response_model=schemas.Token)
def generate_token(form_data: schemas.TokenRequest, db: Session = Depends(dependencies.get_db)):
    return auth.generate_token(db=db, form_data=form_data)

@app.post("/token/validate/", response_model=schemas.TokenData)
def validate_token(token: schemas.Token, db: Session = Depends(dependencies.get_db)):
    return auth.validate_token(db=db, token=token)