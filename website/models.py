from flask_login import UserMixin
from datetime import datetime
from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    posts = db.relationship("Post")


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.String(256))
    body = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=datetime.now())
