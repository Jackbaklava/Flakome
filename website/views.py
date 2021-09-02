from flask import Blueprint, render_template, request
from flask_login import login_required


views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    return render_template("home.html")


@views.route("create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        pass
    
    return render_template("create-post.html")
