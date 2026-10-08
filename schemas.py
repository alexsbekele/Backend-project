from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class TaskCreate(BaseModel):
    title: str
    completed: bool = False
    description: str | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int
    description: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TaskUpdate(BaseModel):
    title: str
    completed: bool
    description: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str