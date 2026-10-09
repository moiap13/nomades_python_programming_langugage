import os
import json


# import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials, firestore

from repositories.user_firestore import (
  get_user_by_email, 
  get_user_by_uid, 
  add_user,
  get_user_by_firestore_id
)
from helpers.random_password_generator import generate_password as generate_salt
from helpers.security import hash_pwd
from helpers.decorators import authenticated

app = Flask(__name__)

CURR_DIR: str = os.path.dirname(__file__)
CREDS_FILE: str = os.path.join(CURR_DIR, "config", "creds.json")
CSV_FILE: str = os.path.join(CURR_DIR, "users.csv")
FIRESTORE_CREDS: str = os.path.join(CURR_DIR, "config", "firestore-creds.json")

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
    return render_template("login/register.html", form_values={})


@app.route("/signup", methods=["POST"])
def register_post():
    """
    Register function should add a new user to the users.csv file
    """
    # get the user uid from form
    uid: str = request.form.get("uid", "").strip()
    # get the user password from form
    pwd: str = request.form.get("pwd", "").strip()
    # get the user password 2 from form
    pwd2: str = request.form.get("pwd2", "").strip()
    # get the remaining infomrations (firstname, lastname, email)
    firstname: str = request.form.get("firstname", "").strip()
    lastname: str = request.form.get("lastname", "").strip()
    email: str = request.form.get("email", "").strip()

    # validate that all the informations are sets
    if uid == '' or not pwd or not pwd2 or not firstname or not lastname or not email:
        # return "Error: Please fill all the form's fields"
        return render_template("login/register.html", error="Error: Please fill all the form's fields")

    if "@" not in email:
        return "Error: Invalid email address"
    
    # Validate that the two passwords are the same
    # if different return "Password mismatch"
    if pwd != pwd2:
        return "Error: Passwords mismatch"

    # verify user is unique in database
    if get_user_by_uid(uid, db) or get_user_by_email(email, db):
        return "Error: user already exists (email and / or uid should be unique)"

    # Open in "a" mode the users csv file using the constant CSV_FILE
    salt: str = generate_salt(True, False, False, False, 10)
    h_pwd: str = hash_pwd(pwd, salt)

    user: dict[str, str] = add_user({
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "uid": uid,
        "pwd": h_pwd,
        "salt": salt
    }, db)

    session["loggedin"] = True
    session["uid"] = uid
    session["firestore_id"] = user["id"]

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
        user: dict[str, str] = get_user_by_uid(uid, db)
        if user:
            h_pwd: str = hash_pwd(pwd, user["salt"])
            if user["pwd"] == h_pwd:
              # if login successful -> return "Login successful"
              session["loggedin"] = True
              session["uid"] = uid
              session["firestore_id"] = user["id"]

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
    user: dict[str, str] = get_user_by_firestore_id(session["firestore_id"], db)
    return render_template("user/userinfo.html", user=user)

# TODO: Create user modify route to the route /user/modify
# The user modify routes gets the user's: 
#   firsntame, lastname, uid, email 
# from the form defined in user/usermodify.html and update the database
# /!\ this route should be private
# /!\ Check that uid and email are unique when updating them
# The post method should update the user in the database and redirect to user info


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
