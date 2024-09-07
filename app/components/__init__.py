from dataclasses import dataclass

from app.models import Book


@dataclass
class Bookshelf:
    title: str
    books: list[Book]
