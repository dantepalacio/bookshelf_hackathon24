import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from pathlib import Path


load_dotenv()
print(os.getenv("DATABASE_URII"))

app = Flask(__name__, root_path=str(Path(__file__).parent.parent))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.secret_key = os.getenv("SECRET_KEY", "").encode()
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "/login"# type: ignore
login_manager.init_app(app)


from app.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    return render_template("pages/index.j2")

from .routes import register_routes
from .template import main

register_routes(app)
main(app)
