from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import json
from .models import Post, current_datetime
from .db_config import CharLimits
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
        given_title = data.get("title")
        given_body = data.get("body")

        title_limits = CharLimits.post["title"]
        body_limits = CharLimits.post["body"]

        if (len(given_title) < title_limits["min"] or len(given_title) > title_limits["max"]):
            flash(f"Title must be between {title_limits['min']} and {title_limits['max']} characters long.",
                category="error")

        elif (len(given_body) < body_limits["min"] or len(given_body) > body_limits["max"]):
            flash(f"Body must be between {body_limits['min']} and {body_limits['max']} characters long.",
                category="error")

        else:
            new_post = Post(title=given_title, body=given_body, author=current_user, date=current_datetime())
            db.session.add(new_post)
            db.session.commit()
            flash("Post created.", category="success")
            return redirect(url_for("views.home"))

        return redirect(url_for("views.create_post", title=given_title, body=given_body))

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
        post.title = data.get("title")
        post.body = data.get("body")
        db.session.add(post)
        db.session.commit()
        flash("Post successfully edited", category="success")
        return redirect(url_for("views.home"))

    title = post.title
    body = post.body
    return render_template("edit-post.html", title_to_display=title, body_to_display=body)
