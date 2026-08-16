from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email : str
    password : str

class UserResponse(BaseModel):
    id : int
    email : str

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title : str
    description : str | None = None
    completed : bool

class TaskResponse(BaseModel):
    id : int
    title : str
    description : str
    completed : bool = False
    owner_id : int

    class Config:
        from_attributes = True
