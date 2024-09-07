from flask import Flask
from .admin import admin


def register_routes(app: Flask):
    app.register_blueprint(admin, url_prefix="/admin")
