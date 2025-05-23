from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, Field

class ReviewModel(BaseModel):
    uid: uuid.UUID
    rating: int = Field(lt=5)
    review_text: str
    user_uid: Optional[uuid.UUID] = Field(default=None)
    book_uid: Optional[uuid.UUID] = Field(default=None)
    created_at: datetime
    updated_at: datetime

class ReviewCreateModel(BaseModel):
    rating: int = Field(lt=5)
    review_text: str