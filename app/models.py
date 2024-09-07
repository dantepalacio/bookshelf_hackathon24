from datetime import date
from typing import Literal
from flask_login import UserMixin
from sqlalchemy import ForeignKey, Integer, String, DateTime, func
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
    description: Mapped[str]

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


class BaseUserBook(db.Model):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), primary_key=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey(Book.id), primary_key=True)


class UserFavBook(BaseUserBook):
    __tablename__ = "fav_book"
    __table_args__ = {"extend_existing": True}


class UserWishList(BaseUserBook):
    __tablename__ = "wish_list"
    __table_args__ = {"extend_existing": True}


class UserBookTrade(BaseUserBook):
    __tablename__ = "book_for_trade"
    __table_args__ = {"extend_existing": True}


class UserBookshelf(BaseUserBook):
    __tablename__ = "personal_bookshelf"
    __table_args__ = {"extend_existing": True}
    is_read: Mapped[bool] = mapped_column(default=False)


class Status(db.Model):
    __tablename__ = "status"
    __table_args__ = {"extend_existing": True}
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Comment(db.Model):
    __tablename__ = "comment"
    __table_args__ = {"extend_existing": True}
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    status: Mapped[int] = mapped_column(Integer, ForeignKey(Status.id), default=0)
    for_book: Mapped[bool] = mapped_column(default=False) #False - for posts, True - for books
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


def main():
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    main()
