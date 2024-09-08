from operator import or_
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from app.components import Bookshelf
from app.models import Book, User, UserBookshelf

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template("pages/login.j2")

    email = request.form.get("email")
    password = request.form.get("password")

    # Ищем пользователя в базе данных
    user = User.query.filter_by(email=email).first()

    if user and user.password == password:
        login_user(user)
        return redirect(url_for("index"))
    else:
        return render_template("pages/login.j2")


@auth_bp.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for("index"))
    return "", 403


@auth_bp.route("/me")
@login_required
def me():
    bookshelf = list(
        map(
            lambda a: a[0],
            (
                UserBookshelf.query.with_entities(UserBookshelf.book_id)
                .filter(UserBookshelf.id == current_user.id)
                .all()
            ),
        )
    )
    if len(bookshelf) > 1:
        books = Book.query.filter(or_(*(Book.id == id for id in bookshelf))).all()
    elif len(bookshelf) == 1:
        books = Book.query.filter(Book.id == bookshelf[0]).all()
    else:
        books = []
    sections = [
        Bookshelf(books=books, title="Личная полка"),
    ]
    return render_template("pages/me.j2", sections=sections)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "GET":
        return render_template("pages/register.j2")
    return "", 403
