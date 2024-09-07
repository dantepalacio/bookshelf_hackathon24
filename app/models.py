from datetime import date
from typing import Literal
from flask_login import UserMixin
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db, app

UserRole = Literal["user", "librarian", "moderator", "admin"]


class User(db.Model, UserMixin):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(String(255))
    address: Mapped[UserRole] = mapped_column(String(255))
    birthday: Mapped[date]


class Author(db.Model):
    __tablename__ = "authors"
    __table_args__ = {"extend_existing": True}
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))


class Book(db.Model):
    __tablename__ = "books"
    __table_args__ = {"extend_existing": True}
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    rating: Mapped[float]
    year: Mapped[int]
    book_cover: Mapped[str] # URL
    publisher: Mapped[str]
    author: Mapped[str]
    views: Mapped[int] = mapped_column(default=0)

class Genre(db.Model):
    __tablename__ = "genre"
    __table_args__ = {"extend_existing": True}
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))


class GenreBook(db.Model):
    genre_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(Genre.id), primary_key=True
    )
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey(Book.id), primary_key=True)
    
    book = relationship(Book, uselist=False, backref="genres")
    genre = relationship(Genre, uselist=False, backref="books")

class AuthorBook(db.Model):
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(Author.id), primary_key=True
    )
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey(Book.id), primary_key=True)


class Player(db.Model):
    __tablename__ = "player"
    __table_args__ = {"extend_existing": True}
    id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), primary_key=True)
    rating: Mapped[int] = mapped_column(default=1000)
    in_game: Mapped[bool] = mapped_column(default=False)
    waiting: Mapped[bool] = mapped_column(default=False)


def main():
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    main()
