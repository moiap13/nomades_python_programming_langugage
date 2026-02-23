import os
import sys

ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

import hashlib
import uuid

from flask import Blueprint, request, session, flash, redirect, url_for, render_template

from helpers.decorators import authenticated
from helpers.random_password_generator import generate_password as generate_salt

# TODO: remove csv database
from database.csv_database import (
    get_user_by_email,
    get_user_by_username,
    add_user_to_csv,
)

from database.user_repository import UserRepository

from models.user import User

UPLOAD_DIR: str = os.path.join(ROOT_DIR, "static", "uploads")

login_bp: Blueprint = Blueprint("login", __name__)
_user_repository = UserRepository()


@login_bp.route("/register", methods=["get", "post"])
def register():
    """
    Register function should add a new user to the users.csv file
    """
    if request.method == "POST":
        # TODO: Adapt using the user repository

        # get the user uid from form
        username: str = request.form["uid"]
        # get the user password from form
        pwd: str = request.form.get("pwd")
        # get the user password 2 from form
        pwd2: str = request.form.get("pwd2")
        # handle firstname, email, lastname, avatar data
        firstname: str = request.form.get("firstname")
        lastname: str = request.form.get("lastname")
        email: str = request.form.get("email")
        avatar = request.files.get("avatar")

        # Validation
        # check firstname, lastname, avatar can't be null
        if (
            not username
            or not pwd
            or not pwd2
            or not firstname
            or not lastname
            or not email
        ):
            flash("Error: Please fill out the full formular", "danger")
            return redirect(url_for("login.register"))

        # Validate that the two passwords are the same
        if pwd != pwd2:
            # if different return "Password mismatch"
            flash("Error: Passwords mismatch", "danger")
            return redirect(url_for("login.register"))

        # check that avatar is from jpg, jpeg or png format
        # if not correct type -> flash please provide a valid image
        if avatar and avatar.content_type not in [
            "image/jpeg",
            "image/jpg",
            "image/png",
        ]:
            flash("Error: The file must be an image", "danger")
            return redirect(url_for("login.register"))

        # validate email (check that @ char is present in string)
        # if not a correct email -> flash please provide a valid email
        if "@" not in email:
            flash("Error: Please provide a valid email", "danger")
            return redirect(url_for("login.register"))

        # if get_user_by_username(username):
        #     flash(f"Error: User with username={username} already exists", "danger")
        #     return redirect(url_for("register"))
        if _user_repository.get_user_by_username(username):
            flash(f"Error: User with username={username} already exists", "danger")
            return redirect(url_for("login.register"))

        salt: str = generate_salt(True, False, False, False, 10)
        h_pwd: str = hashlib.sha256((pwd + salt).encode()).hexdigest()

        if avatar:
            ext: str = avatar.filename.split(".")[-1]
            filename: str = f"{uuid.uuid4()}.{ext}"
            avatar.save(os.path.join(UPLOAD_DIR, filename))
        else:
            filename: str = ""

        # Open in "a" mode the users csv file using the constant CSV_FILE
        add_user_to_csv(
            User(firstname, lastname, email, username, salt, h_pwd, filename)
        )

        session["loggedin"] = True
        session["uid"] = username
        flash("User successfully registered", "success")
        return redirect(url_for("user.userinfo"))
    else:
        return render_template("login/register.html")


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    The login functiojn should authenticate a user using his uid and pwd
    """
    if request.method == "POST":
        # TODO: Adapt using the user repository
        uid: str = request.form["uid"]
        pwd: str = request.form["pwd"]

        user: User = _user_repository.get_user_by_username(uid)
        if not user:
            user: User = get_user_by_email(uid)

        if user:
            salt: str = user.salt
            h_pwd: str = hashlib.sha256((pwd + salt).encode()).hexdigest()
            if user.password == h_pwd:
                session["loggedin"] = True
                session["uid"] = uid
                flash("Login successfull", "success")
                if "wanted_route" in session:
                    return redirect(session["wanted_route"])
                return redirect(url_for("user.userinfo"))

        # otw, return "Wrong credentials"
        flash("Wrong credentials", "danger")
        return redirect(url_for("login.login"))

    else:
        return render_template("login/login.html")


@login_bp.route("/logout")
@authenticated
def logout():
    session.clear()
    flash("User logged out successfully", "success")
    return redirect(url_for("login.login"))
