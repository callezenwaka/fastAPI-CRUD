from fastapi import HTTPException, status
from src.database.models import Review
from src.users.service import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.reviews.schemas import ReviewCreateModel

userService = UserService()
bookService = BookService()

class ReviewService:
    async def add_review_to_book(
            self,
            user_email: str, 
            book_uid: str, 
            review_data: ReviewCreateModel, 
            session: AsyncSession
        ):
        try:
            book = await bookService.get_book(book_uid=book_uid,session=session)
            user = await userService.get_user_by_email(email=user_email,session=session)

            review_data_dict = review_data.model_dump()
            new_review = Review(**review_data_dict)

            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found"
                )
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            new_review.user = user
            new_review.book = book
            session.add(new_review)
            await session.commit()

            return new_review
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Oops . . . Something went wrong!"
            )