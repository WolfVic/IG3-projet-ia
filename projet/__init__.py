import os

from flask import Flask
from flask_login import LoginManager

from .models import User, db, init_db
from .views import auth_bp, game_bp, admin_bp
from .utils import parse_users
import logging as lg

# APP SETUP

app = Flask(__name__)
app.config.from_object("config")
app.config.update(
    {
        "SQLALCHEMY_DATABASE_URI": os.environ.get(
            "SQLALCHEMY_DATABASE_URI",
            app.config["SQLALCHEMY_DATABASE_URI"],
        ),
        "SQLALCHEMY_TRACK_MODIFICATIONS": os.environ.get(
            "SQLALCHEMY_TRACK_MODIFICATIONS",
            app.config["SQLALCHEMY_TRACK_MODIFICATIONS"],
        ),
        "SECRET_KEY": os.environ.get("SECRET_KEY", app.config["SECRET_KEY"]),
        "ADMIN_USERS": parse_users(os.environ.get("ADMIN_USERS", "")),
    }
)

if app.config["ENV"] == "development":
    lg.basicConfig(level=lg.DEBUG)

# IMPORT BLUEPRINT AND REGISTER


app.register_blueprint(game_bp)
app.add_url_rule("/", endpoint="index")

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

# DB SETUP


db.init_app(app)

# SETUP LOGIN MANAGER

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# CLI COMMANDS


@app.cli.command("init_db")
def cmd_init_db():
    """Command to initialize database with flask"""
    init_db()
