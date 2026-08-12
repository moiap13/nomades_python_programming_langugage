import os, sys

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
sys.path.append(ROOT_DIR)

from uuid import uuid4
import hashlib

from flask import Blueprint, request, render_template, session, flash, redirect, url_for

from config.firestore_config import db
from forms.login import RegisterForm, LoginForm
from repositories.users_repository_firestore import (
  get_user_by_uid, 
  get_user_by_email, 
  add_user
)
from exceptions.user import UserNotFoundError
from models.user import User

UPLOAD_FOLDER: str = os.path.join(ROOT_DIR, 'static', 'uploads')

login_bp = Blueprint('login', __name__)

@login_bp.route("/signup", methods=["GET"])
def register_get():
    """
    Register function should add a new user to the users.csv file
    """
    form = RegisterForm(request.form)
    return render_template("login/register.html", form_values={}, form=form)


# Handle missing profile picture
@login_bp.route("/signup", methods=["POST"])
def register_post():
    """
    Register function should add a new user to the users.csv file
    """
    form = RegisterForm(request.form, data=request.files)

    if not form.validate():
        # return "Error: Please fill all the form's fields"
        return render_template("login/register.html", form=form)
    
    # 1. Get the data
    uid: str = form.uid.data
    firstname: str = form.firstname.data
    lastname: str = form.lastname.data
    email: str = form.email.data
    pwd: str = form.pwd.data
    pp: "FileStorage" | None  = form.pp.data

    # (BONUS): Check if user already exists in csv file, if so -> return "User already exists"
    try:
      get_user_by_uid(db, uid)
    except UserNotFoundError: 
        pass
    else:
        return render_template("login/register.html", error=f"Error: User with uid={uid} already exists", form_values=request.form)

    try:
      get_user_by_email(db, email)
    except UserNotFoundError: 
        pass
    else:
      return render_template("login/register.html", error=f"Error: User with email={email} already exists", form_values=request.form)

    # handle image
    if pp:
      pp_ext = pp.filename.split('.')[-1]
      pp_filename = f'{uuid4()}.{pp_ext}'
      pp.save(os.path.join(UPLOAD_FOLDER, pp_filename))

    # Open in "a" mode the users csv file using the constant CSV_FILE
    # d = dict(request.form)
    # d.pop("pwd2")
    # add_user(d)
    # user_dict: dict[str, str] = {
    #     "firstname": firstname,
    #     "lastname": lastname,
    #     "email": email,
    #     "uid": uid,
    #     "pwd": pwd,
    # } | ({"pp_filename": pp_filename} if pp else {})


    user: User = add_user(db, User(
      firstname=firstname,
      lastname=lastname,
      uid=uid,
      email=email,
      pwd=pwd,
      pp_filename=pp_filename if pp else ""
    ))
    session["loggedin"] = True
    session["uid"] = uid
    session["firestore_id"] = user.firestore_id
    # session["user"] = user_dict
    
    flash("User successfully registered", "success")
    return redirect(url_for("user.user_info"))

@login_bp.route("/signin", methods=["GET", "POST"])
def login():
    """
    The login functiojn should authenticate a user using his uid and pwd
    """
    form = LoginForm(request.form)

    if request.method == "POST" and form.validate():
        uid_email: str = form.uid.data
        pwd: str = form.pwd.data

        try:
            user: User = get_user_by_uid(db, uid_email)
        except UserNotFoundError:
            try: 
                user: User = get_user_by_email(db, uid_email)
            except UserNotFoundError:
                return "Wrong credentials"
                            
        h_pwd: str = hashlib.sha256((pwd+user.salt).encode()).hexdigest()
        if user.pwd == h_pwd:
            # if login successful -> return "Login successful"
            session["loggedin"] = True
            session["uid"] = uid_email
            session["firestore_id"] = user.firestore_id
            flash("Login successfull", "success")
            return redirect(url_for("user.user_info"))

        flash("Wrong credentials", "danger")
    return render_template("login/login.html", form=form)

@login_bp.route("/signout")
def logout():
    session["loggedin"] = False
    session.pop("loggedin")
    session.clear()
    flash("User successfully logged out", "success")
    return redirect(url_for("login.login"))