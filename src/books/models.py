# src/books/models.py
from sqlmodel import SQLModel, Field, Column, Relationship
from datetime import date, datetime
# from src.users import models
import sqlalchemy.dialects.postgresql as pg 
from typing import Optional
import uuid

class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, 
            nullable=False, 
            primary_key=True, 
            default=uuid.uuid4
        ),
    )
    title: str = Field(nullable=False)
    author: str = Field(nullable=False)
    publisher: str = Field(nullable=False)
    published_date: date = Field(nullable=False)
    page_count: int = Field(nullable=False)
    language: str = Field(nullable=False)
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP, 
            nullable=False,
            default=datetime.now
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP, 
            nullable=False,
            default=datetime.now
        )
    )
    user: Optional["User"] = Relationship(back_populates="books")

    def __repr__(self):
        return f"<Book {self.title}>"