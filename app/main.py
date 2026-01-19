from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from . import models, crud, schemas
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return{"message": "Таблицы созданы, сервер работает1!"}

@app.post("/users/", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email = user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user

@app.post("/users/{user.id}/tasks/", response_model=schemas.TaskOut)
def create_task_for_user(
    user_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)
):
    return crud.create_user_task(db=db, task=task, user_id=user_id)

@app.patch("/tasks/{task_id}", response_model = schemas.TaskOut)
def update_task_status(task_id: int, completed: bool, db: Session = Depends(get_db)):
    db_task = crud.update_task(db, task_id=task_id, completed=completed)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = crud.delete_task(db, task_id=task_id)
    if not success: 
        raise HTTPException(status_code=404, detail='Задача не найдена')
    return {"message": "Задача успешно удалена"}
