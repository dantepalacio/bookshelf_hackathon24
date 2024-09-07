from app import db, app
from app.models import Player

def find_opponent(user_id):
    player = Player.query.filter(Player.id == user_id).one()
    players = Player.query.filter(Player.waiting == True).all()
    possible_opponents = [p for p in players if p.id != player.id]
    if not possible_opponents:
        return None
    possible_opponents.sort(key=lambda p: abs(players[p].rating - player.rating))
    return possible_opponents[0]