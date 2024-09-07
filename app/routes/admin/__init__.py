from app import db
from app.models import Book
from flask import Blueprint, request

admin = Blueprint("admin", __name__)



@admin.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # a = request.form.get('s')
        book_title = request.form.get('book_title')
        author = request.form.get('author')
        year = request.form.get('year')
        publisher = request.form.get('publisher')
        book_cover = request.form.get('book_cover')

        book = Book(name=book_title,# type: ignore
                    rating=0.0, # type: ignore
                    year=year,# type: ignore
                    book_cover=book_cover,# type: ignore
                    publisher=publisher,# type: ignore
                    author=author)# type: ignore
        
        db.session.add(book)
        db.session.commit()

        return "200",200
    return "",400
