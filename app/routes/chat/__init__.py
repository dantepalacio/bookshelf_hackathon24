from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.models import db, User, Message
from app import app
from datetime import datetime
from flask_socketio import SocketIO, emit, join_room

# Инициализация Blueprint
chat_bp = Blueprint("chat", __name__)

socketio = SocketIO(app)

# Маршрут для страницы с чатом
@chat_bp.route('/')
@login_required
def chat():
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('pages/chat.html', users=users)

# Маршрут для получения истории переписки с пользователем
@chat_bp.route('/chat/history/<int:user_id>')
@login_required
def chat_history(user_id):
    recipient = User.query.get_or_404(user_id)
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.recipient_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.recipient_id == current_user.id))
    ).order_by(Message.timestamp).all()

    history = [{"sender": msg.sender_id, "content": msg.content, "timestamp": msg.timestamp} for msg in messages]
    return jsonify(history)

# WebSocket для отправки сообщений в реальном времени
@socketio.on('send_message')
def handle_send_message(data):
    recipient_id = data['recipient_id']
    content = data['message']
    
    # Создаем сообщение в базе данных
    new_message = Message(sender_id=current_user.id, recipient_id=recipient_id, content=content, timestamp=datetime.utcnow()) #type: ignore
    db.session.add(new_message)
    db.session.commit()

    # Отправляем сообщение обоим пользователям
    room = f"chat_{min(current_user.id, recipient_id)}_{max(current_user.id, recipient_id)}"
    emit('receive_message', {'sender': current_user.id, 'message': content}, room=room) # type: ignore

# WebSocket подключение к комнате чата
@socketio.on('join')
def on_join(data):
    recipient_id = data['recipient_id']
    room = f"chat_{min(current_user.id, recipient_id)}_{max(current_user.id, recipient_id)}"
    join_room(room)
