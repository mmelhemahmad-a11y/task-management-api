from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique = True, nullable = False, index = True)
    password = Column(String, nullable = False, index = True)
    tasks = relationship("Task", back_populates = "owner")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable = False, index = True)
    description = Column(String, nullable = True, index = True)
    completed = Column(Boolean, default = False, index = True)
    owner_id = Column(Integer, ForeignKey("users.id"), index = True)
    owner = relationship("User", back_populates = "tasks")
