from os import name
from app import db, app
from app.models import User, Book, Genre, GenreBook

import random

def get_most_popular_books():
    # books_under_2000 = Book.query.filter(Book.year<=2000)
    books_trending = Book.query.order_by(Book.views).limit(10).all()
    print(books_trending)


def get_book_by_genres(genres: list):
    # Book.query.filter(Book.genres)
    pass






        
        
    # get_books_from_db()

