from app import db
from app.models import Book, Review
from flask import Blueprint, abort, render_template

books = Blueprint("books", __name__)


@books.route("/<int:id>")
def item(id: int):
    book: Book | None = Book.query.get(id)
    if not book:
        return abort(404)
    Book.query.filter(Book.id == id).update({Book.views: book.views + 1})
    db.session.commit()

    reviews = (
        Review.query.filter(Review.book_id == id).order_by(Review.created_at).all()
    )

    return render_template("pages/book.j2", book=book, reviews=reviews)
