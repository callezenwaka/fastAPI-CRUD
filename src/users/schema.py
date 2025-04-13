# src/users/schema.py
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class UserCreateModel(BaseModel):
    username: str = Field(min_length=6)
    email: str = Field(max_length=40)
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    password: str = Field(min_length=6)

class UserModel(BaseModel):
    uid: UUID
    username: str = Field(nullable=False)
    email: str = Field(nullable=False)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime

class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)