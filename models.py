from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime, func, Index
from sqlalchemy.orm import relationship
from pydantic import EmailStr

from database import Base

class User(Base):
    __tablename__ = "users"

    id  = Column(Integer, primary_key = True, index = True)
    name = Column(String(100), nullable = False)
    email = Column(String(255), unique = True, nullable = False)
    
    password_hash = Column(String(255), nullable = False)
    
    tasks = relationship("Task", back_populates="user")
    

class Task(Base):
    __tablename__ = "tasks"

    id  = Column(Integer, primary_key = True)
    title = Column(String(255), nullable = False)
    completed = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tasks")
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    __table_args__ = (Index("ix_tasks_user_id_created_at", "user_id", "created_at"),)