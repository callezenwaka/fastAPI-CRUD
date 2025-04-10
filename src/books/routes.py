from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from typing import List
from src.books.schema import Book, BookUpdateModel
from src.books.data import books

bookRouter = APIRouter()

@bookRouter.get("/", response_model=List[Book])
async def get_all_books():
    return books


@bookRouter.post("/", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: Book) -> dict:
    new_book = book_data.model_dump()

    books.append(new_book)

    return new_book


@bookRouter.get("/{book_id}")
async def get_book(book_id: str) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@bookRouter.put("/{book_id}")
async def update_book(book_id: str, book_data: BookUpdateModel) -> dict:

    for book in books:
        if book['id'] == book_id:
            book['title'] = book_data.title
            book['publisher'] = book_data.publisher
            book['page_count'] = book_data.page_count
            book['language'] = book_data.language

            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@bookRouter.delete("/{book_id}",status_code=status.HTTP_201_CREATED)
async def delete_book(book_id: str) -> dict:
    for book in books:
        if book["id"] == book_id:
            books.remove(book)

            return {"message": f"Book id {book_id} removed!"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")