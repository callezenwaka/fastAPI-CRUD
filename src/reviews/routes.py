from fastapi import APIRouter, Depends
from src.database import get_session
from src.database.models import User
from src.reviews.schemas import ReviewCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.reviews.service import ReviewService
from src.users.routes import get_current_user

reviewRouter = APIRouter()
reviewService = ReviewService()

@reviewRouter.post('/book/{book_uid}')
async def add_review_to_book(
    book_uid: str, 
    review_data: ReviewCreateModel, 
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
    ):
    print(f"book_uid: {book_uid}")
    print(f"current_user: {current_user}")
    print(f"review_data: {review_data}")
    new_review = await reviewService.add_review_to_book(
        user_email = current_user.email,
        review_data = review_data,
        book_uid = book_uid,
        session = session
    )

    return new_review
