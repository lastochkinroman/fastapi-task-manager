from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from . import models, crud, schemas
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return{"message": "Таблицы созданы, сервер работает!"}

@app.post("/users/", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email = user.email)
    if db_user:
        raise HTTPException(status_code=400, detai="Email уже зарегистрирован")
    
    return crud.create_user(db=db, user=user)