from typing import Optional, Dict

from fastapi import FastAPI
from enum import Enum

xyz = FastAPI()

BOOKS: dict[str, dict[str, str] | dict[str, str] | dict[str, str] | dict[str, str] | dict[str, str]] = {
    'book_1': {'title1': 'title one', 'author': 'author one'},
    'book_2': {'title1': 'title two', 'author': 'author two'},
    'book_3': {'title1': 'title three', 'author': 'author three'},
    'book_4': {'title1': 'title4', 'author': 'author4'},
    'book_5': {'title1': 'title5', 'author': 'author5'},

}


class DirectionName(str, Enum):
    north = "North",
    south = "South",
    east = "East",
    west = "West"


# @xyz.get("/")
# async def read_books():
#    return BOOKS


@xyz.get("/")
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        new_book = BOOKS.copy()
        del new_book[skip_book]
        return new_book
    return BOOKS


@xyz.get("/books/mybook")
async def read_my_favorite_book():
    return {"title": "my_favorite_book"}


@xyz.get("/books/{book_id}")
async def read_title_of_book(book_id: int):
    return {"title": book_id}


@xyz.get("/directions/{direction_name}")
async def read_name_direction(direction_name: DirectionName):
    if direction_name == DirectionName.west:
        return {"a: direction_name", "sub: left"}
    if direction_name == DirectionName.north:
        return {"b: direction_name", "sub: up"}
    if direction_name == DirectionName.south:
        return {"c: direction_name", "sub: down"}
    return {"d: direction_name", "sub:right"}


@xyz.get("/{book_name}")
async def read_one_book(book_name: str):
    return BOOKS[book_name]


@xyz.post("/")
async def create_book(book_title, book_author):
    current_book_id = 0
    if len(BOOKS) > 0:
        for num in BOOKS:
            x = int(num.split('_')[-1])
            if x > current_book_id:
                current_book_id = x
    BOOKS[f'book_{current_book_id + 1}'] = {'title': book_title, 'author': book_author}


@xyz.put("/{book_name}")
async def update_book(book_name: str, book_title: str, book_author: str):
    book_information = {'title': book_title, 'author': book_author}
    BOOKS[book_name] = book_information
    return book_information


@xyz.delete("/{book_name}")
async def delete_book(book_name):
    del BOOKS[book_name]
    return f'The {book_name} is deleted.'


@xyz.get("/assignment/")
async def read_book_assignment(book_name: str):
    return BOOKS[book_name]


@xyz.delete("/assignment/")
async def delete_book_assignment(book_name: str):
    del BOOKS[book_name]
    return BOOKS
