from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


load_dotenv()

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # create_database(app)

    # login_manager = LoginManager()
    # login_manager.login_view = "auth.login"
    # login_manager.login_message_category = "error"
    # login_manager.init_app(app)

    # from .models import User


    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.get(user_id)


    return app


def create_database(app):
    if not os.path.exists("website/" + DB_NAME):
        db.create_all(app=app)
