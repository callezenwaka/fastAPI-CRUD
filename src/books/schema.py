from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional
from src.reviews.schema import ReviewModel
from src.tags.schema import TagModel
import uuid

class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime

    # class Config:
    #     orm_mode = True

class BookDetailModel(Book):
    reviews: List[ReviewModel]
    tags:List[TagModel]

class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

# For updates to existing books
class BookUpdateModel(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    published_date: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = None