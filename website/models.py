from flask_login import UserMixin
from datetime import datetime
from .db_config import CharLimits
from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(CharLimits.user["username"]["max"]), unique=True)
    password = db.Column(db.String(CharLimits.user["password"]["max"]))
    posts = db.relationship("Post", backref="author")


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String(CharLimits.post["title"]["max"]))
    body = db.Column(db.String(CharLimits.post["body"]["max"]))
    date = db.Column(db.DateTime(timezone=True), default=datetime.now())
