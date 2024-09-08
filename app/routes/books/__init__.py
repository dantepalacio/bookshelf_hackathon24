from flask_login import current_user
from sqlalchemy import and_
from app import db
from app.models import Book, Review, UserBookshelf
from flask import Blueprint, abort, render_template

books = Blueprint("books", __name__)


@books.route("/<int:id>")
def item(id: int):
    book: Book | None = Book.query.get(id)
    if not book:
        return abort(404)
    Book.query.filter(Book.id == id).update({Book.views: book.views + 1})
    db.session.commit()

    book.is_in_bookshelf = bool(
        UserBookshelf.query.filter(
            and_(UserBookshelf.book_id == id, UserBookshelf.id == current_user.id)
        ).first()
    )

    reviews = (
        Review.query.filter(Review.book_id == id).order_by(Review.created_at).all()
    )

    return render_template("pages/book.j2", book=book, reviews=reviews)
