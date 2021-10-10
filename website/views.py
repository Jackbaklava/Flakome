from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import json
from .models import Post, current_datetime
from .utils import validate_post
from . import db


views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    return render_template("home.html", posts=Post.query.order_by(Post.date.desc()).all())


@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post(title="", body=""):
    if request.method == "POST":
        data = request.form
        title_submitted = data.get("title")
        body_submitted = data.get("body")
        post_is_validated = validate_post(title_submitted, body_submitted)

        if post_is_validated:
            new_post = Post(title=title_submitted, body=body_submitted, author=current_user, date=current_datetime())
            db.session.add(new_post)
            db.session.commit()
            flash("Post created.", category="success")
            return redirect(url_for("views.home"))

        return redirect(url_for("views.create_post", title=title_submitted, body=body_submitted))

    return render_template(
        "create-post.html",
        title_to_display=request.args.get("title"),
        body_to_display=request.args.get("body"),
    )


@views.route("/delete-post", methods=["GET", "POST"])
@login_required
def delete_post():
    if request.method == "GET":
        return redirect(url_for("views.home"))

    res = json.loads(request.data)
    post_id = res["postId"]

    try:
        post = Post.query.get(post_id)
        if post.author_id == current_user.id:
            db.session.delete(post)
            db.session.commit()
            flash("Post successfully deleted.", category="success")
    except:
        return redirect(url_for("views.home"))

    return ""



@views.route("/edit-post/<post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    try:
        post = Post.query.get(post_id)
        if post.author_id != current_user.id:
            raise Exception("User does not own the post.")
    except:
        return redirect(url_for("views.home"))

    if request.method == "POST":
        data = request.form
        post_is_validated = validate_post(data.get("title"), data.get("body"))

        if post_is_validated:
            post.title = data.get("title")
            post.body = data.get("body")
            db.session.add(post)
            db.session.commit()
            flash("Post successfully edited", category="success")
            return redirect(url_for("views.home"))

    title = post.title
    body = post.body
    return render_template("edit-post.html", title_to_display=title, body_to_display=body)
