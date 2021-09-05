from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Post
from .db_config import CharLimits
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

        title_limits = CharLimits.post["title"]
        body_limits = CharLimits.post["body"]

        if len(title) < title_limits["min"] or len(title) > title_limits["max"]:
            flash(f"Title must be between {title_limits['min']} and {title_limits['max']} characters long.", category="error")

        elif len(body) < body_limits["min"] or len(body) > body_limits["max"]:
            flash(f"Body must be between {body_limits['min']} and {body_limits['max']} characters long.", category="error")

        else:
            new_post = Post(title=title, body=body, author=current_user)
            db.session.add(new_post)
            db.session.commit()
            flash("Post created.", category="success")
            return redirect(url_for("views.home"))

        return redirect(url_for("views.create_post"))
    
    return render_template("create-post.html")
