import os, sys
ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from hashlib import sha256
from uuid import uuid4

from flask import Blueprint, request, render_template, redirect, url_for, flash, session

from config.firestore_connection import db
from forms.login import RegisterForm, LoginForm
from helpers.firestore_funcs import get_user_by_uid, USERS_COLLECTION
from helpers.password_generator import generate_password as generate_salt
from repositories.user import UserRepository
from models.user import User
from exceptions.user import UserNotFoundError

UPLOAD_DIR: str = os.path.join(ROOT_DIR, 'static', 'uploads')
PP_DIR: str = os.path.join(UPLOAD_DIR, 'pp')

login_bp = Blueprint('login', __name__)
user_repositry = UserRepository()

@login_bp.route('/register')
def register():
    """
    Register function should add a new user to the users.csv file
    """
    # WTForms: Adapt to use WTForms instead of request.form
    form = RegisterForm(request.form, data=request.files)
    if request.method == "POST" and form.validate(): # WTForms: validate the from
        # 1. Get the data
        # WTForms: get the data from the wtf form object
        # get the user uid from form
        uid: str = form.uid.data
        # get the user password from form
        pwd: str = form.pwd.data
        
        firstname: str = form.firstname.data
        lastname: str = form.lastname.data
        email: str = form.email.data
        age: int = form.age.data

        pp = form.pp.data

        # 3. Logic
        # (BONUS): Check if user already exists in csv file, if so -> return "User already exists"
        if get_user_by_uid(uid, db) != None:
            return "Error: User already exists"
        
        salt: str = generate_salt(True, False, False, False, 10)
        h_pwd: str = sha256((pwd+salt).encode()).hexdigest()

        pp_ext: str = pp.filename.split(".")[-1]
        pp_filename: str = f"{uuid4()}.{pp_ext}"
        pp.save(os.path.join(PP_DIR, pp_filename))

        _, doc = db.collection(USERS_COLLECTION).add({
            "uid": uid,
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "age": age,
            "pwd": h_pwd,
            "salt": salt,
            'pp_filename': pp_filename
        })

        session["loggedin"] = True
        session["uid"] = uid
        session["firestore_id"] = doc.id

        flash(f"User {uid} successfully registered", "success")

        return redirect(url_for("user.user_info"))
    else:
        # GET
        return render_template("login_wtf/register.html", form=form) # WTForms: pass the form object to the front

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    The login functiojn should authenticate a user using his uid and pwd
    """
    # WTForms: Adapt to use WTForms instead of request.form
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate(): # WTForms: validate the from
        # 1. Get the datas
        # WTForms: get the data from the wtf form object
        uid: str = form.uid.data
        pwd: str = form.pwd.data

        # 3. Logic
        # Open in "r" mode the users csv file using the constant CSV_FILE
        try:
          user: User = user_repositry.get_by_uid(uid)
        except UserNotFoundError as e:
          flash("Wrong credentials", "danger")
          return render_template("login_wtf/login.html", form=form)
        except ValueError as e:
            # Send email to webmaster
            # save in log that database is corrupted
            # redirect to interal server error page
            return "", 500
        
        salt: str = user.salt
        h_pwd: str = sha256((pwd + salt).encode()).hexdigest()
        if user.pwd == h_pwd:
            # if login successful -> return "Login successful"
            flash("Login successful", "success")
            session["loggedin"] = True
            session["uid"] = uid
            session["firestore_id"] = user.id

            return redirect(url_for("user.user_info"))

        # otw, return "Wrong credentials"
        return "Wrong Credentials"
    else:
        return render_template("login_wtf/login.html", form=form) # WTForms: pass the form object to the front

@login_bp.route("/logout")
def logout():
    # logout the user; think about session
    session["loggedin"] = False
    session.pop("loggedin")
    session.clear() 
    # redirect to login route
    flash("logout successful", "success")
    return redirect(url_for('login.login'))
