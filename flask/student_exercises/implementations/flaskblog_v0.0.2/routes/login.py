import os, sys

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
sys.path.append(ROOT_DIR)

from uuid import uuid4

from flask import Blueprint, request, render_template, session, flash, redirect, url_for

from forms.login import RegisterForm, LoginForm

from exceptions.user import UserNotFoundError
from models.user import User
from services.user import UserService

from services.login import LoginService
from exceptions.login import WrongCredentialsError


UPLOAD_FOLDER: str = os.path.join(ROOT_DIR, 'static', 'uploads')

login_bp = Blueprint('login', __name__)

user_service = UserService()
login_service = LoginService()

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
    pp: "FileStorage" | None  = form.pp.data

    # handle image
    if pp:
      pp_ext = pp.filename.split('.')[-1]
      pp_filename = f'{uuid4()}.{pp_ext}'
      pp.save(os.path.join(UPLOAD_FOLDER, pp_filename))

    user: User = user_service.create_user(User(
      uid=form.uid.data,
      firstname=form.firstname.data,
      lastname=form.lastname.data,
      email=form.email.data,
      pwd=form.pwd.data,
      pp_filename=pp_filename if pp else ""
    ))

    session["loggedin"] = True
    session["uid"] = user.uid
    session["firestore_id"] = user.firestore_id
    
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
            user: User = login_service.login(uid_email, pwd)
        except (UserNotFoundError, WrongCredentialsError):
            flash("Wrong credentials", "danger")
            return render_template("login/login.html", form=form)
                            
        session["loggedin"] = True
        session["uid"] = uid_email
        session["firestore_id"] = user.firestore_id
        flash("Login successfull", "success")
        return redirect(url_for("user.user_info"))
    
    return render_template("login/login.html", form=form)

@login_bp.route("/signout")
def logout():
    session["loggedin"] = False
    session.pop("loggedin")
    session.clear()
    flash("User successfully logged out", "success")
    return redirect(url_for("login.login"))