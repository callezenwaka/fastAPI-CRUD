from datetime import datetime
from sqlmodel import Column, Field, SQLModel
import sqlalchemy.dialects.postgresql as pg 
import uuid

class User(SQLModel, table=True):
    __tablename__ = 'users'

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, 
            nullable=False, 
            primary_key=True, 
            default=uuid.uuid4
        ),
    )
    username: str = Field(nullable=False)
    email: str = Field(nullable=False)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    role: str = Field(sa_column=Column(
        pg.VARCHAR, 
        nullable=False, 
        server_default="user"
    ))
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)
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

    def __repr__(self):
        return f"<User {self.username}>"