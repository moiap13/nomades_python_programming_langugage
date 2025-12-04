import sys
import os

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
sys.path.append(ROOT_DIR)

from hashlib import sha256

from flask import Blueprint, request, session, render_template, flash, redirect, url_for

from config.firestore_connection import db

from helpers.errors import UserNotFoundError
from helpers.files import generate_pp_filename
from helpers.firestore_funcs import get_user_by_uid, get_user_by_email
from helpers.password_generator import generate_password as generate_salt

from models.user import User

from forms.login import RegisterForm, LoginForm

UPLOAD_DIR: str = os.path.join(ROOT_DIR, "static", "uploads")

login_bp: Blueprint = Blueprint("login", __name__)


@login_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Register function should add a new user to the users.csv file
    """
    form = RegisterForm(request.form, data=request.files)
    if request.method == "POST" and form.validate():
        # 1. Get the data
        # get the user uid from form
        uid: str = form.uid.data
        # get the user password from form
        pwd: str = form.pwd.data
        # get the user password 2 from form
        firstname: str = form.firstname.data
        lastname: str = form.lastname.data
        email: str = form.email.data
        age: int = form.age.data
        pp = form.pp.data

        if pp:
            pp_filename: str = generate_pp_filename(pp.filename)
            pp.save(os.path.join(UPLOAD_DIR, pp_filename))

        # 3. Logic
        # (BONUS): Check if user already exists by uid
        # Check if user already exists by email
        try:
            get_user_by_uid(uid, db)
        except UserNotFoundError:
            pass
        else:
            flash(f"User with uid={uid} already exists", "danger")
            return render_template("login/register.html", form=form)

        try:
            get_user_by_email(email, db)
        except UserNotFoundError:
            pass
        else:
            flash(f"User with email={email} already exists", "danger")
            return render_template("login/register.html", form=form)

        # Add user to the database
        # Add the new user to the CSV file
        salt: str = generate_salt(True, False, False, False, 10)
        h_pwd: str = sha256((pwd + salt).encode()).hexdigest()
        _, doc_ref = db.collection("users").add(
            User(
                uid=uid,
                pwd=h_pwd,
                salt=salt,
                firstname=firstname,
                lastname=lastname,
                email=email,
                age=age,
                pp=pp_filename if pp else "",
            ).to_dict(include_id=False)
        )

        session["loggedin"] = True
        session["uid"] = uid
        session["firestore_id"] = doc_ref.id
        flash("User successfully created", "success")
        return redirect(url_for("user.user_info"))
    else:
        # GET
        return render_template("login_wtf/register.html", form=form)


# Actually the login loops throught each users of the database, implement a query that gives the user by uid directly
@login_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    The login functiojn should authenticate a user using his uid and pwd
    """
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        # 1. Get the datas
        uid_email: str = form.uid.data
        pwd: str = form.pwd.data

        # 3. Logic
        # Open in "r" mode the users csv file using the constant CSV_FILE
        try:
            user: dict[str, str | int] = get_user_by_uid(uid_email, db)
        except UserNotFoundError:
            try:
                user: dict[str, str | int] = get_user_by_email(uid_email, db)
            except UserNotFoundError:
                flash("Wrong credentials", "danger")
                return render_template("login_wtf/login.html", form=form)

        salt: str = user.salt
        h_pwd: str = sha256((pwd + salt).encode()).hexdigest()
        if user.pwd == h_pwd:
            # if login successful -> return "Login successful"
            session["loggedin"] = True
            session["uid"] = user.uid
            session["firestore_id"] = user.firestore_id
            flash("Login successful", "success")
            return redirect(url_for("user.user_info"))

        # otw, return "Wrong credentials"
        flash("Wrong credentials", "danger")
        return render_template("login_wtf/login.html", form=form)
    else:
        return render_template("login_wtf/login.html", form=form)


@login_bp.route("/logout")
def logout():
    session["loggedin"] = False
    session.pop("loggedin")
    session.clear()
    flash("Logout successful", "success")

    return redirect(url_for("login.login"))
