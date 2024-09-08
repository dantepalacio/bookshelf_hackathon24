from app import app, db
from flask import Blueprint, abort, redirect, request, jsonify
from app.models import (
    Post,
    UserFavBook,
    UserBookTrade,
    UserWishList,
    Comment,
    Review,
    UserBookshelf,
)
from flask_login import current_user

from app.nsfw_detection.cv.check import check_post

api = Blueprint("api", __name__)


@api.route("/post", methods=["POST"])
def post():

    if not request:
        return jsonify(""), 400

    text = request.form.get("text")
    image = request.form.get("image_url")

    if text is None and image is None:
        return jsonify(""), 400

    new_post = Post(text=text, image=image, user_id=current_user.id)

    db.session.add(new_post)
    db.session.commit()

    return jsonify(""), 200


@api.route("/comment", methods=["POST"])
def comment():

    if not request:
        return jsonify(""), 400

    text = request.form.get("text")
    post_id = request.form.get("post_id")

    if text is None or post_id is None:
        return jsonify(""), 400

    new_comment = Comment(text=text, post_id=post_id, user_id=current_user.id)

    db.session.add(new_comment)
    db.session.commit()

    return jsonify(""), 200


@api.route("/review", methods=["POST"])
def review():
    text = request.form.get("text")
    book_id = request.form.get("book_id")

    if text is None or book_id is None:
        return abort(400)


    content = {'text':text, 'image':None,'video':None}
    detection_result = check_post(content)
    print(detection_result)

    review_status = detection_result['text'][0]['is_explicit']

    if review_status == 'publish':
        result_status = 1
    else:
        result_status = 2

    new_review = Review(text=text, book_id=book_id, user_id=current_user.id, status=result_status)

    db.session.add(new_review)
    db.session.commit()

    return redirect(request.headers.get("Referer"))


@api.route("/add_to_favs", methods=["POST"])
def add_to_fav():

    if not request:
        return jsonify(""), 400

    book_id = request.form.get("book_id")

    if book_id is None:
        return jsonify(""), 400

    newfavbook = UserFavBook.query.filter(
        UserFavBook.id == current_user.id, UserFavBook.book_id == book_id
    ).one()
    if newfavbook:
        return jsonify(""), 400

    newfavbook = UserFavBook(id=current_user.id, book_id=int(book_id))

    db.session.add(newfavbook)
    db.session.commit()

    return jsonify(""), 200


@api.route("/rm_from_favs", methods=["POST"])
def rm_from_fav():

    if not request:
        return jsonify(""), 400

    book_id = request.form.get("book_id")

    if book_id is None:
        return jsonify(""), 400

    favbook = UserFavBook.query.filter(
        UserFavBook.id == current_user.id, UserFavBook.book_id == book_id
    ).one()

    if favbook:
        db.session.delete(favbook)
        db.session.commit()

    return jsonify(""), 200


@api.route("/add_to_wish", methods=["POST"])
def add_to_wish():

    if not request:
        return jsonify(""), 400

    book_id = request.form.get("book_id")

    if book_id is None:
        return jsonify(""), 400

    newwishbook = UserWishList.query.filter(
        UserWishList.id == current_user.id, UserWishList.book_id == book_id
    ).one()
    if newwishbook:
        return jsonify(""), 400

    newwishbook = UserWishList(id=current_user.id, book_id=int(book_id))

    db.session.add(newwishbook)
    db.session.commit()

    return jsonify(""), 200


@api.route("/rm_from_wish", methods=["POST"])
def rm_from_wish():

    if not request:
        return jsonify(""), 400

    book_id = request.form.get("book_id")

    if book_id is None:
        return jsonify(""), 400

    wishbook = UserWishList.query.filter(
        UserWishList.id == current_user.id, UserWishList.book_id == book_id
    ).one()

    if wishbook:
        db.session.delete(wishbook)
        db.session.commit()

    return jsonify(""), 200


@api.route("/add_to_trade", methods=["POST"])
def add_to_trade():

    if not request:
        return jsonify(""), 400

    book_id = request.form.get("book_id")

    if book_id is None:
        return jsonify(""), 400

    newtradebook = UserBookTrade.query.filter(
        UserBookTrade.id == current_user.id, UserBookTrade.book_id == book_id
    ).one()
    if newtradebook:
        return jsonify(""), 400

    newtradebook = UserBookTrade(id=current_user.id, book_id=int(book_id))

    db.session.add(newtradebook)
    db.session.commit()

    return jsonify(""), 200


@api.route("/rm_from_trade", methods=["POST"])
def rm_from_trade():

    if not request:
        return jsonify(""), 400

    book_id = request.form.get("book_id")

    if book_id is None:
        return jsonify(""), 400

    tradebook = UserBookTrade.query.filter(
        UserBookTrade.id == current_user.id, UserBookTrade.book_id == book_id
    ).one()

    if tradebook:
        db.session.delete(tradebook)
        db.session.commit()

    return jsonify(""), 200


@api.route("/add_to_shelf", methods=["POST"])
def add_to_shelf():
    book_id = request.args.get("book")

    if book_id is None:
        return jsonify(""), 400

    newbook = UserBookshelf(id=current_user.id, book_id=int(book_id))

    db.session.add(newbook)
    db.session.commit()

    return "На полке", 200


@api.route("/rm_from_shelf", methods=["POST"])
def rm_from_shelf():

    if not request:
        return jsonify(""), 400

    book_id = request.form.get("book_id")

    if book_id is None:
        return jsonify(""), 400

    newbook = UserBookshelf.query.filter(
        UserBookshelf.id == current_user.id, UserBookshelf.book_id == book_id
    ).one()

    if newbook:
        db.session.delete(newbook)
        db.session.commit()

    return jsonify(""), 200
