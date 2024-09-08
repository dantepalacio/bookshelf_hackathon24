import os

from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required
from flask_socketio import SocketIO, emit, join_room
from flask_migrate import Migrate
from pathlib import Path

load_dotenv()

app = Flask(__name__, root_path=str(Path(__file__).parent.parent))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.secret_key = os.getenv("SECRET_KEY", "").encode()
db = SQLAlchemy(app)
migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.login_view = "/login"  # type: ignore
login_manager.init_app(app)


from app.controllers import get_most_popular_books, get_book_by_genres
from app.models import User
from app.constants.genres import CLASSICAL_GENRE


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from app.components import Bookshelf


@app.route("/")
def index():
    sections = [
        Bookshelf(books=get_most_popular_books(), title="Самые популярные книги"),
        Bookshelf(books=get_book_by_genres(CLASSICAL_GENRE), title="Вечная классика"),
    ]
    return render_template("pages/index.j2", sections=sections)



from .routes import register_routes
from .template import main

register_routes(app)
main(app)