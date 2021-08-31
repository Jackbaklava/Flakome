from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .import db


auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))

    if request.method == "POST":
        data = request.form
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()
        
        if user:   
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Successfully logged in.", category="success")
                return redirect(url_for("views.home"))

            flash("Incorrect password.", category="error")

        else:
            flash("Incorrect username.", category="error")

    return render_template("login.html")


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))

    if request.method == "POST":
        data = request.form
        username = data.get("username")
        password = data.get("password")
        password_confirmation = data["password_confirmation"]
        
        if len(username) < 2:
            flash("Username must be atleast 2 characters long.", category="error")
        elif len(username) > 63:
            flash("Username must be shorter than 64 characters.", category="error")

        elif len(password) < 6:
            flash("Password must be atleast 6 characters long.", category="error")
        elif len(password) > 127:
            flash("Password must be shorter than 128 characters.", category="error")
        elif password != password_confirmation:
            flash("Passwords don't match. Try again.", category="error")

        elif User.query.filter_by(username=username).first():
            flash("An account with this username already exists. Please login.", category="error")
            return redirect(url_for("auth.login"))

        else:
            new_user = User(username=username, password=generate_password_hash(password, "sha256", salt_length=32))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created.", category="success")

            return redirect(url_for("views.home"))

    return render_template("sign-up.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Successfully logged out.", category="success")
    return redirect(url_for("auth.login"))
