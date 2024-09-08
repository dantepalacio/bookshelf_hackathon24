from flask import Blueprint, redirect, render_template, request, jsonify, url_for
from flask_login import login_user, logout_user, current_user
from app.models import User
from werkzeug.security import check_password_hash

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


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "GET":
        return render_template("pages/register.j2")
    return "", 403
