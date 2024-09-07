from flask import Flask
from .filters import add_filters


def main(app: Flask):
    add_filters(app)
