import os
import sys

ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

import hashlib
import uuid

from flask import Blueprint, request, session, flash, redirect, url_for, render_template

from helpers.decorators import authenticated
from helpers.random_password_generator import generate_password as generate_salt

from exceptions.user import UserNotFoundError

from database.user_repository import UserRepository
from forms.login import RegisterForm

from models.user import User

UPLOAD_DIR: str = os.path.join(ROOT_DIR, "static", "uploads")

login_bp: Blueprint = Blueprint("login", __name__)
_user_repository = UserRepository()


@login_bp.route("/register", methods=["get", "post"])
def register():
    """
    Register function should add a new user to the users.csv file
    """
    form = RegisterForm(request.form, data=request.files)
    if request.method == "POST" and form.validate():
        username: str = form.uid.data
        pwd: str = form.pwd.data
        firstname: str = form.firstname.data
        lastname: str = form.lastname.data
        email: str = form.email.data
        avatar = form.avatar.data

        try:
            _user_repository.get_user_by_username(username)
        except UserNotFoundError:
            pass
        else:
            flash(f"Error: User with username={username} already exists", "danger")
            return render_template("login/register.html", form=form)

        salt: str = generate_salt(True, False, False, False, 10)
        h_pwd: str = hashlib.sha256((pwd + salt).encode()).hexdigest()

        if avatar:
            ext: str = avatar.filename.split(".")[-1]
            filename: str = f"{uuid.uuid4()}.{ext}"
            avatar.save(os.path.join(UPLOAD_DIR, filename))
        else:
            filename: str = ""

        # Open in "a" mode the users csv file using the constant CSV_FILE
        firestore_id: str = _user_repository.add_user(
            User("", firstname, lastname, email, username, salt, h_pwd, filename)
        )

        session["loggedin"] = True
        session["uid"] = username
        session["firestore_id"] = firestore_id
        flash("User successfully registered", "success")
        return redirect(url_for("user.userinfo"))

    return render_template("login/register.html", form=form)


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    The login functiojn should authenticate a user using his uid and pwd
    """
    if request.method == "POST":
        uid: str = request.form["uid"]
        pwd: str = request.form["pwd"]

        try:
            user: User = _user_repository.get_user_by_username(uid)
        except UserNotFoundError:
            try:
                user: User = _user_repository.get_user_by_email(uid)
            except UserNotFoundError:
                flash("Wrong credentials", "danger")
                return redirect(url_for("login.login"))

        salt: str = user.salt
        h_pwd: str = hashlib.sha256((pwd + salt).encode()).hexdigest()
        if user.password == h_pwd:
            session["loggedin"] = True
            session["uid"] = uid
            session["firestore_id"] = user.id
            flash("Login successfull", "success")
            if "wanted_route" in session:
                return redirect(session["wanted_route"])
            return redirect(url_for("user.userinfo"))

    else:
        return render_template("login/login.html")


@login_bp.route("/logout")
@authenticated
def logout():
    session.clear()
    flash("User logged out successfully", "success")
    return redirect(url_for("login.login"))
