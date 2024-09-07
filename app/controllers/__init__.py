from sqlalchemy import or_
from app.models import Book, GenreBook


def get_most_popular_books() -> list[Book]:
    books_trending = Book.query.order_by(Book.views.desc()).limit(10).all()
    return books_trending


def get_book_by_genres(genres: list[int]) -> list[Book]:
    books = list(
        map(
            lambda g: g.book,
            GenreBook.query.filter(or_(*(GenreBook.genre_id == i for i in genres)))
            .limit(20)
            .all(),
        )
    )
    return books
