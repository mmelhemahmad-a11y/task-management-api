from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas, models, utils, oauth2
from database import engine, get_db
from fastapi.security import OAuth2PasswordRequestForm

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/register/", response_model = schemas.UserResponse)
def register(user : schemas.UserCreate, db : Session = Depends(get_db)):
    db_query = db.query(models.User).filter(models.User.email == user.email).first()
    if db_query:
        raise HTTPException(
            status = status.HTTP_400_BAD_REQUEST,
            detail = "Email already registered"
        )
    
    hash_pwd = utils.hash_password(user.password)
    new_user = models.User(
        email = user.email,
        password = hash_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login/")
def login(form_data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    db_query = db.query(models.User).filter(models.User.email == form_data.username).first()
    the_exception =  HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect email or password"
        )
    if db_query is None:
        raise the_exception
    verified_password = utils.verify_password(form_data.password, db_query.password)
    if not verified_password :
        raise the_exception
    access_token = oauth2.create_access_token(data = {"user_id" : db_query.id})
    return {"access_token" : access_token, "token_type" : "bearer"}

@app.post("/tasks/", response_model = schemas.TaskResponse)
def task_create(task : schemas.TaskCreate, db : Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    task = models.Task(
        owner_id = current_user.id,
        title = task.title,
        description = task.description,
        completed = task.completed
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.get("/tasks/", response_model = list[schemas.TaskResponse])
def get_tasks(db : Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    return tasks

@app.get("/tasks/{task_id}", response_model = schemas.TaskResponse)
def get_tasks_id(task_id : int, db : Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "task not found"
        )
    if task.owner_id != current_user.id:
       raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "task not found"
       )
    return task

@app.put("/tasks/{task_id}", response_model = schemas.TaskResponse)
def task_update(task_id : int, updated_task :schemas.TaskCreate, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "task not found"
        )
    if task.owner_id != current_user.id:
        raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail = "task not found"
                )
    task.title = updated_task.title
    task.description = updated_task.description
    task.completed = updated_task.completed
        
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
def deleted_task(task_id : int, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    not_found_exception = HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "task not found"
    )
    if task is None:
        raise not_found_exception
    if task.owner_id != current_user.id:
        raise not_found_exception
    db.delete(task)
    db.commit()
    return {"detail" : "Task deleted successfully"}
    
