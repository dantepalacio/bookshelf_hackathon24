from flask import Blueprint, render_template


quiz = Blueprint("quiz", __name__)


@quiz.route("/", methods=["GET"])
def get_quizz():
    return render_template("pages/quiz.j2")
