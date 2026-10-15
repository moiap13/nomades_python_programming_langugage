import os, sys
ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from uuid import uuid4

from flask import Blueprint, render_template, request, flash, session, redirect, url_for

from config.firestore_connection import db
from helpers.random_password_generator import generate_password as generate_salt
from helpers.security import hash_pwd
from exceptions.user import UserNotFoundError
from forms.login import RegisterForm
from models.user import User
from repositories.user_firestore import (
   get_user_by_uid,
   get_user_by_email,
   add_user
)

UPLAOD_DIR: str = os.path.join(ROOT_DIR, "static", "uploads")

login_bp: Blueprint = Blueprint("login", __name__)

@login_bp.route("/signup", methods=["GET"])
def register_get():
    """
    Register function should add a new user to the users.csv file
    """
    form = RegisterForm(request.form)
    return render_template("login_wtf/register.html", form=form)

@login_bp.route("/signup", methods=["POST"])
def register_post():
    """
    Register function should add a new user to the users.csv file
    """
    form = RegisterForm(request.form, data=request.files)

    if not form.validate():
      return render_template("login_wtf/register.html", form=form)

    uid: str = form.uid.data.strip()
    pwd: str = form.pwd.data.strip()
    firstname: str = form.firstname.data.strip()
    lastname: str = form.lastname.data.strip()
    email: str = form.email.data.strip()
    pp = form.pp.data

    # verify user is unique in database
    try:
      get_user_by_uid(uid, db)
    except UserNotFoundError:
      pass
    else:
      flash("Error: User with uid={uid} already exists", "danger")
      return render_template("login_wtf/register.html", form=form)

    try:
      get_user_by_email(email, db)
    except UserNotFoundError:
      pass
    else:
      flash("Error: User with email={email} already exists", "danger")
      return render_template("login_wtf/register.html", form=form)

    if pp:
      pp_ext: str = pp.filename.split('.')[-1]
      pp_filename: str = f"{uuid4()}.{pp_ext}"
      pp.save(os.path.join(UPLAOD_DIR, pp_filename))

    # Open in "a" mode the users csv file using the constant CSV_FILE
    salt: str = generate_salt(True, False, False, False, 10)
    h_pwd: str = hash_pwd(pwd, salt)

    user: User = add_user(User.from_dict({
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "uid": uid,
        "pwd": h_pwd,
        "salt": salt,
      } | ({"pp_filename": pp_filename} if pp else {})
    ), db)

    session["loggedin"] = True
    session["uid"] = uid
    session["firestore_id"] = user.firestore_id

    # redirect to private route
    flash("User successfully registered", "success")
    return redirect(url_for('user.user_info' ))

@login_bp.route("/signin", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uid: str = request.form.get("uid", "")
        pwd: str = request.form.get("pwd", "")

        if not uid or not pwd:
            return "Error: Please fill out the form"

        # Open in "r" mode the users csv file using the constant CSV_FILE
        try:
          user: User = get_user_by_uid(uid, db)
        except UserNotFoundError:
           flash("Wrong Credential", "danger")
           return render_template("login_wtf/login.html")
           
           
        h_pwd: str = hash_pwd(pwd, user.salt)
        if user.pwd == h_pwd:
          # if login successful -> return "Login successful"
          session["loggedin"] = True
          session["uid"] = uid
          session["firestore_id"] = user.firestore_id

          flash("Login successful", "success")
          return redirect(url_for("user.user_info"))
            
        return "Wrong credentials"
    else:
        return render_template("login_wtf/login.html")

@login_bp.route("/signout")
def logout():
    # create signout logic
    session["loggedin"] = False
    session.pop("loggedin")
    session.clear()
    flash("User successfully logged out", "success")
    return redirect(url_for("login.login"))