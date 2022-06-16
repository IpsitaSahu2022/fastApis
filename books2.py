from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(bookTitle='Description of book', max_length=100, min_lenght=1)
    rating: int = Field(gt=-1, lt=101)

    class Config:
        Schema_extra = {
            "example": {
                "id": "275a3da-3418-484c-9497-fcb00a2685c7",
                "title": "Electrical Drives",
                "author": "JK. Morgan",
                "description": "Fundamentals on Drives"
            }
        }


BOOKS = []


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if len(BOOKS) < 1:
        create_books_no_api()

    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books

    return BOOKS


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/{/book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]
        raise raise_item_cannot_be_found_exception()


@app.delete("/{/book_id}")
async def delete_book(book_id: UUID):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f'the ID:{book_id} is deleted'
    raise raise_item_cannot_be_found_exception()


def create_books_no_api():
    book_1 = Book(id="8175a3da-3418-484c-9497-fcb00a2685c6",
                  title="Title 1",
                  author="Author 1",
                  description="Description 1",
                  rating=60)
    book_2 = Book(id="8175a3da-3418-484c-9497-fcb00a2685c7",
                  title="Title 2",
                  author="Author 2",
                  description="Description 2",
                  rating=80)
    book_3 = Book(id="8175a3da-3418-484c-9497-fcb00a2685c8",
                  title="Title 3",
                  author="Author 3",
                  description="Description 3",
                  rating=80)

    book_4 = Book(id="8175a3da-3418-484c-9497-fcb00a2685c9",
                  title="Title 4",
                  author="Author 4",
                  description="Description 4",
                  rating=90)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)


def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404, detail="book not found",
                         headers={"x-header-error": "nothing to be seen at the UUID"})
