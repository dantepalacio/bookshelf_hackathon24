from flask import Flask
from .admin import admin
from .books import books
from .chat import chat_bp
from .auth import auth_bp
from .api import api

def register_routes(app: Flask):
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(books, url_prefix="/books")
    app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(auth_bp)
    app.register_blueprint(api, url_prefix="/api")
