import os
import json
from uuid import uuid4

# import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials, firestore

from repositories.user_firestore import (
  get_user_by_email, 
  get_user_by_uid, 
  add_user,
  get_user_by_firestore_id,
  update_user
)
from helpers.random_password_generator import generate_password as generate_salt
from helpers.security import hash_pwd
from helpers.decorators import authenticated
from models.user import User
from exceptions.user import UserNotFoundError
from forms.login import RegisterForm

app = Flask(__name__)

CURR_DIR: str = os.path.dirname(__file__)
CREDS_FILE: str = os.path.join(CURR_DIR, "config", "creds.json")
CSV_FILE: str = os.path.join(CURR_DIR, "users.csv")
FIRESTORE_CREDS: str = os.path.join(CURR_DIR, "config", "firestore-creds.json")
UPLAOD_DIR: str = os.path.join(CURR_DIR, "static", "uploads")

with open(CREDS_FILE) as config_file:
  config: dict[str, str] = json.load(config_file)

app.config["SECRET_KEY"] = config["secret_key"]


cred = credentials.Certificate(FIRESTORE_CREDS)
firebase_admin.initialize_app(cred)
db = firestore.client()
print(db)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup", methods=["GET"])
def register_get():
    """
    Register function should add a new user to the users.csv file
    """
    form = RegisterForm(request.form)
    return render_template("login_wtf/register.html", form=form, form_values={})


@app.route("/signup", methods=["POST"])
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
    return redirect(url_for('user_info' ))


@app.route("/signin", methods=["GET", "POST"])
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
           return render_template("login/login.html")
           
           
        h_pwd: str = hash_pwd(pwd, user.salt)
        if user.pwd == h_pwd:
          # if login successful -> return "Login successful"
          session["loggedin"] = True
          session["uid"] = uid
          session["firestore_id"] = user.firestore_id

          flash("Login successful", "success")
          return redirect(url_for("user_info"))
            
        return "Wrong credentials"
    else:
        return render_template("login/login.html")

@app.route("/signout")
def logout():
    # create signout logic
    session["loggedin"] = False
    session.pop("loggedin")
    session.clear()
    flash("User successfully logged out", "success")
    return redirect(url_for("login"))

@app.route("/secret")
@authenticated
def private():
    return f"Welcome to the private part {session['uid']}"

# create a new private route to displays user informations
# THis route should be private (not public, meaning secured by authentication)
# The user infomrations will be the one given by the register:
# - Firstname
# - Lastname
# - Email
# - Username
# - Password
@app.route("/user/info")
@authenticated
def user_info():
    user: User = get_user_by_firestore_id(session["firestore_id"], db)
    return render_template("user/userinfo.html", user=user.to_dict())

# Create user modify route to the route /user/modify
# The user modify routes gets the user's: 
#   firsntame, lastname, uid, email 
# from the form defined in user/usermodify.html and update the database
# /!\ this route should be private
# /!\ Check that uid and email are unique when updating them
# The post method should update the user in the database and redirect to user info
@app.route("/user/modify", methods=["GET", "POST"])
@authenticated
def user_modify():
  current_user: User = get_user_by_firestore_id(session["firestore_id"], db)

  if request.method == "POST":
    user_data: User = User.from_dict(
      {k:v for k, v in request.form.items() if v != ""} 
      | {"firestore_id": current_user.firestore_id}
    )

    if user_data.uid and user_data.uid != current_user.uid:
      try:
        get_user_by_uid(user_data.uid, db)
      except UserNotFoundError:
        pass
      else:
        flash(f"uid: {user_data.uid} already exists", "danger")
        return render_template("/user/usermodify.html", user=request.form)

    if user_data.email and user_data.email != current_user.email:
      try:
        get_user_by_email(user_data.email, db)
      except UserNotFoundError:
        pass
      else:
        flash(f"email: {user_data.email} already exists", "danger")
        return render_template("/user/usermodify.html", user=request.form)

    update_user(user_data, db)
    flash("User successfully updated", "success")
    return redirect(url_for('user_info'))

  return render_template("/user/usermodify.html", user=current_user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
