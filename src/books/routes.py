from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from src.books.schema import Book, BookUpdateModel
from src.database import get_db
from src.books.services import BookService

bookRouter = APIRouter()
bookService = BookService()

@bookRouter.get("/", response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_db)):
    books = await bookService.get_all_books(session)

    return books


@bookRouter.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_book(book_data: Book, session: AsyncSession = Depends(get_db)) -> dict:
    new_book = await bookService.create_book(book_data, session)

    return new_book


@bookRouter.get("/{book_uid}")
async def get_book(book_uid: str, session: AsyncSession = Depends(get_db)) -> dict:
    book = await bookService.get_book(book_uid, session)

    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@bookRouter.put("/{book_uid}")
async def update_book(book_uid: str, book_data: BookUpdateModel, session: AsyncSession = Depends(get_db)) -> dict:
    update_book = await bookService.update_book(book_uid, book_data, session)

    if update_book:
        return update_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@bookRouter.delete("/{book_uid}",status_code=status.HTTP_201_CREATED)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_db)) -> dict:
    delete_book = await bookService.delete_book(book_uid, session)
    
    if delete_book:
        return {"message": f"Book id {book_uid} removed!"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")