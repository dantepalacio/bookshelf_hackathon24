from flask import Flask
from .admin import admin
from .books import books


def register_routes(app: Flask):
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(books, url_prefix="/books")
