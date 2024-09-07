from app import app, db
from flask import Blueprint, render_template, request, jsonify
from app.models import Post, UserFavBook, UserBookTrade
from flask_login import current_user

api = Blueprint("api", __name__)

@api.route("/get_posts", methods=["GET"])
def get_posts():
    
    if not request:
        return jsonify(""), 400
    
    posts = Post.query.order_by(Post.created_at.desc()).limit(20).all()
    print(posts)

    return jsonify({'results': posts}), 200


@api.route("/post", methods=['POST'])
def post():

    if not request:
        return jsonify(""), 400
    
    text = request.form.get('text')
    image = request.form.get('image_url')

    if text is None and image is None:
        return jsonify(""), 400

    new_post = Post(text=text, image=image, user_id=current_user.id)

    with app.app_context():
        db.session.add(new_post)
        db.session.commit()

    return jsonify(""), 200


@api.route("/get_fav_books", methods=["GET"])
def get_fav():

    if not request:
        return jsonify(""), 400
    
    user_id = current_user.id

    favbooks = UserFavBook.query.filter(UserFavBook.id == user_id)

    return jsonify({'results': favbooks}), 200


@api.route("/add_to_favs", methods=["POST"])
def add_to_fav():

    if not request:
        return jsonify(""), 400
    
    book_id = request.form.get('book_id')

    if book_id is None:
        return jsonify(""), 400

    newfavbook = UserFavBook(id = current_user.id, book_id = int(book_id))

    with app.app_context():
        db.session.add(newfavbook)
        db.session.commit()

    return jsonify(""), 200


@api.route("/get_trade_books", methods=["GET"])
def get_fav():

    if not request:
        return jsonify(""), 400
    
    user_id = current_user.id

    favbooks = UserBookTrade.query.filter(UserBookTrade.id == user_id)

    return jsonify({'results': favbooks}), 200