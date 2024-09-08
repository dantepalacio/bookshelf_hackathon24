from flask import Blueprint, render_template, request, jsonify
from app.models import Book
from app import db
from sqlalchemy import func


search_bp = Blueprint("search", __name__)


def search_book(query):
    # search_query = func.to_tsquery('english', query)
    return Book.query.filter(Book.search_vector.match(query)).all()  # type:ignore


@search_bp.route("/", methods=["GET"])
def search():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "No search query provided"}), 400

    results = search_book(query)
    print(results)

    return render_template("pages/search.j2", books=results)
