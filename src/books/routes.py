# src/books/routes.py
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from src.books.schema import Book, BookCreateModel, BookUpdateModel
from src.database import get_session
from src.books.service import BookService
from src.utils.dependency import AccessTokenBearer, RoleChecker
from src.books.schema import BookDetailModel
from src.errors.error import BookNotFound

bookRouter = APIRouter()
bookService = BookService()
accessTokenBearer = AccessTokenBearer()
roleChecker = Depends(RoleChecker(['admin', 'user']))

@bookRouter.get("/", response_model=List[Book], dependencies=[roleChecker])
async def get_all_books(
    session: AsyncSession = Depends(get_session), 
    token_details: dict = Depends(accessTokenBearer),
    ):
    books = await bookService.get_all_books(session)

    return books

@bookRouter.get("/user/{user_uid}", response_model=List[Book], dependencies=[roleChecker])
async def get_books_by_user_id(
    user_uid: str,
    session: AsyncSession = Depends(get_session), 
    token_details: dict = Depends(accessTokenBearer),
    ):
    books = await bookService.get_books_by_user_id(user_uid, session)

    return books

@bookRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Book, dependencies=[roleChecker])
async def create_a_book(
    book_data: BookCreateModel, 
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(accessTokenBearer),
    ) -> dict:
    user_uid = token_details.get('user')['user_uid']
    new_book = await bookService.create_book(book_data, user_uid, session)

    return new_book


@bookRouter.get("/{book_uid}", response_model=BookDetailModel, dependencies=[roleChecker])
async def get_book(
    book_uid: str, 
    session: AsyncSession = Depends(get_session),
     _: dict = Depends(accessTokenBearer),
    ) -> dict:
    book = await bookService.get_book(book_uid, session)

    if book is None:
        raise BookNotFound()
    else:
        return book


@bookRouter.put("/{book_uid}", response_model=Book, dependencies=[roleChecker])
async def update_book(
    book_uid: str, 
    book_data: BookUpdateModel, 
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(accessTokenBearer),
    ) -> dict:
    update_to_book = await bookService.update_book(book_uid, book_data, session)

    if update_to_book is None:
        raise BookNotFound()
    else:
        return update_to_book
        
@bookRouter.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[roleChecker])
async def delete_book(
    book_uid: str, 
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(accessTokenBearer),
    ):
    book_to_delete = await bookService.delete_book(book_uid, session)
    print(f"book_to_delete: {book_to_delete}")
    
    if book_to_delete is None:
        raise BookNotFound()
    else:
        return {}
        