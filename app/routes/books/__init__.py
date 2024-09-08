from flask_login import current_user
from sqlalchemy import and_
from app import db
from app.models import Book, Review, UserBookshelf
from flask import Blueprint, abort, render_template

books = Blueprint("books", __name__)

from app.parser.generation import generate_batches_summary, generate_overall_summary
from app.parser.parser import parse_book
from app.parser.utils import split_text_overlap, google_search


def generate(query, person="Студент"):
    google_result = google_search(query)
    parse_result = parse_book(google_result)

    book_batches = split_text_overlap(
        parse_result, max_fragment_length=4000, overlap_length=400
    )

    batches_sumarries = []
    for batch in book_batches:
        temp_result = generate_batches_summary(batch)

        batches_sumarries.append(temp_result)
        batches_sumarries_string = " ".join(batches_sumarries)

    overall_summary = generate_overall_summary(batches_sumarries_string, person)

    print(f"Result: {overall_summary}")
    return overall_summary


@books.route("/<int:id>")
def item(id: int):
    book: Book | None = Book.query.get(id)
    if not book:
        return abort(404)
    Book.query.filter(Book.id == id).update({Book.views: book.views + 1})
    db.session.commit()

    if current_user.is_authenticated:
        book.is_in_bookshelf = bool(
            UserBookshelf.query.filter(
                and_(UserBookshelf.book_id == id, UserBookshelf.id == current_user.id)
            ).first()
        )
    else:
        book.is_in_bookshelf = False

    reviews = (
        Review.query.filter(and_(Review.book_id == id, Review.status == 1))
        .order_by(Review.created_at)
        .all()
    )

    return render_template("pages/book.j2", book=book, reviews=reviews)


@books.route("/read/<int:id>")
def read(id: int):
    book: Book | None = Book.query.get(id)
    if not book:
        return abort(404)

    text = generate(book.name.lower())
    return render_template("modals/book.j2", book=book, text=text)
