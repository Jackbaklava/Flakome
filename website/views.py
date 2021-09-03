from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from .models import Post
from . import db


views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    return render_template("home.html")


@views.route("create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        data = request.form
        title = data.get("title")
        body = data.get("body")

        new_post = Post(title=title, body=body)
        db.session.add(new_post)
        db.session.commit()
        flash("Post created.", category="success")

        return redirect(url_for("views.home"))
    
    return render_template("create-post.html")
