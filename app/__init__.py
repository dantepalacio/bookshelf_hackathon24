import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from pathlib import Path

load_dotenv()

app = Flask(__name__, root_path=str(Path(__file__).parent.parent))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.secret_key = os.getenv("SECRET_KEY", "").encode()
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return user_id


@app.route("/")
def index():
    print(app.template_folder)
    return render_template("index.j2")
