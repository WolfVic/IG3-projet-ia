from flask_sqlalchemy import SQLAlchemy
from .views import app
import logging as lg

db = SQLAlchemy(app)


def init_db():
    """Initialize Database"""
    db.drop_all()
    db.create_all()
    # TODO Add Models

    victor = User(user_id=1, user_name="Victor", user_password="victorIA")
    joachim = User(user_id=2, user_name="Joachim", user_password="joachimIA")
    db.session.add(victor)
    db.session.add(joachim)
    game1 = Game(1, "2021-10-01", victor, joachim)
    db.session.add(game1)
    db.session.add(State(1, game1, 0, 0, 4, 4))

    db.session.commit()
    lg.warning("Database initialized !")


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(40), nullable=False)

    user_password = db.Column(db.String(256), nullable=False)

    game = db.relationship("Game", backref="game", lazy=True)

    


class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user_id"), nullable=False)

    state = db.relationship("State", backref="state", lazy=True)

    


class State(db.Model):
    state_id = db.Column(db.Integer, primary_key=True)
    board = db.Column(db.String(256), nullable=False)
    pos_player1_X = db.Column(db.Integer, nullable=False)
    pos_player1_Y = db.Column(db.Integer, nullable=False)
    pos_player2_X = db.Column(db.Integer, nullable=False)
    pos_player2_Y = db.Column(db.Integer, nullable=False)

    game_id = db.Column(db.Integer, db.ForeignKey("game_id"), nullable=False)

    
