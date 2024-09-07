from flask import Blueprint, request

admin = Blueprint("admin", __name__)


@admin.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        return ""
    return ""
