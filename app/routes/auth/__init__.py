from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user
from app.models import User
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    if current_user.is_authenticated:
        return jsonify({"message": "Already logged in"}), 200

    data = request.json
    email = data.get('email') # type: ignore
    password = data.get('password') # type: ignore


    # Ищем пользователя в базе данных
    user = User.query.filter_by(email=email).first()

    if user and user.password == password:
        login_user(user)
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401
    
@auth_bp.route('/api/logout', methods=['POST'])
def api_logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({"message": "Logout successful"}), 200
    return jsonify({"message": "Not logged in"}), 400