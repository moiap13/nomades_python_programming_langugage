import os
import json


# import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials, firestore

from repositories.user_csv import CSV_FILE, get_user_by_uid, add_user
from helpers.random_password_generator import generate_password as generate_salt
from helpers.security import hash_pwd
from helpers.decorators import authenticated

# TODO Use firestore (import the firestore functions from the repository folder)

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

    # TODO: verify user is unique in database

    # Open in "a" mode the users csv file using the constant CSV_FILE
    salt: str = generate_salt(True, False, False, False, 10)
    h_pwd: str = hash_pwd(pwd, salt)

    add_user({ # TODO: change for using firestore
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "uid": uid,
        "pwd": h_pwd,
        "salt": salt
    }, CSV_FILE)

    session["loggedin"] = True
    session["uid"] = uid

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
        user: dict[str, str] = get_user_by_uid(uid, CSV_FILE) # TODO: use firestore
        if user:
            h_pwd: str = hash_pwd(pwd, user["salt"])
            if user["pwd"] == h_pwd:
              # if login successful -> return "Login successful"
              session["loggedin"] = True
              session["uid"] = uid

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
    user: dict[str, str] = get_user_by_uid(session["uid"], CSV_FILE) # TODO: use firestore
    return render_template("user/userinfo.html", user=user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
