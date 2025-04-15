# src/users/schema.py
from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, Field
from src.books.schema import Book
from src.reviews.schema import ReviewModel

class UserCreateModel(BaseModel):
    username: str = Field(min_length=6)
    email: str = Field(max_length=40)
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    password: str = Field(min_length=6)

class UserModel(BaseModel):
    uid: uuid.UUID
    username: str = Field(nullable=False)
    email: str = Field(nullable=False)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime

class UserDetailsModel(UserModel):
    books: List[Book]
    reviews: List[ReviewModel]

class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)

class UserMailModel(BaseModel):
    addresses: List[str]