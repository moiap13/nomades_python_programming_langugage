import os
import hashlib
import json

# import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for, flash

from repositories.users_repository import get_user_by_uid, add_user

app = Flask(__name__)

CURR_DIR: str = os.path.dirname(__file__)
CREDS_FILE: str = os.path.join(CURR_DIR, "config", "creds.json")

with open(CREDS_FILE) as config_file:
  config: dict[str, str] = json.load(config_file)

app.config["SECRET_KEY"] = config["secret_key"]

CURR_DIR: str = os.path.dirname(__file__)
CSV_FILE: str = os.path.join(CURR_DIR, "users.csv")

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
    # 1. Get the data
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

    # 2. validate that all the informations are sets
    if uid == '' or not pwd or not pwd2 or not firstname or not lastname or not email:
        # return "Error: Please fill all the form's fields"
        flash("Please fill all the form's fields", "danger")
        return render_template("login/register.html", form_values=request.form)

    if len(firstname) < 3:
        return render_template("login/register.html", error="Error: Please provide a firstname with at least 3 chars", form_values=request.form)

    if "@" not in email:
        return render_template("login/register.html", error="Error: Please provide a valid email adress", form_values=request.form)
    
    # Validate that the two passwords are the same
    # if different return "Password mismatch"
    if pwd != pwd2:
        return render_template("login/register.html", error="Error: Passwords mismatch", form_values=request.form)

    # (BONUS): Check if user already exists in csv file, if so -> return "User already exists"
    if get_user_by_uid(uid) != {}:
        return render_template("login/register.html", error=f"Error: User with uid={uid} already exists", form_values=request.form)
    # TODO: Check email is unique

    # Open in "a" mode the users csv file using the constant CSV_FILE
    # d = dict(request.form)
    # d.pop("pwd2")
    # add_user(d)
    user_dict: dict[str, str] = {
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "uid": uid,
        "pwd": pwd,
    }
    add_user(user_dict)
    session["loggedin"] = True
    session["uid"] = uid
    # session["user"] = user_dict
    
    flash("User successfully registered", "success")
    return redirect(url_for("user_info"))

@app.route("/signin", methods=["GET", "POST"])
def login():
    """
    The login functiojn should authenticate a user using his uid and pwd
    """
    if request.method == "POST":
        # TODO: allow login by email

        uid: str = request.form["uid"]
        pwd: str = request.form["pwd"]

        user: dict[str, str] = get_user_by_uid(uid)
        if user:
            h_pwd: str = hashlib.sha256((pwd+user["salt"]).encode()).hexdigest()
            if user["pwd"] == h_pwd:
                  # if login successful -> return "Login successful"
                  session["loggedin"] = True
                  session["uid"] = uid
                  flash("Login successfull", "success")
                  return redirect(url_for("user_info"))
        return "Wrong credentials"
        
    return render_template("login/login.html")

@app.route("/signout")
def logout():
    session["loggedin"] = False
    session.pop("loggedin")
    session.clear()
    flash("User successfully logged out", "success")
    return redirect(url_for("login"))

@app.route("/secret")
def private():
    if not session.get("loggedin", False):
        return "Please log in first"
    
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
def user_info() -> str:
  if not session.get("loggedin", False):
    flash("Login first", "warning")
    return redirect(url_for("login"))

  user: dict[str, str] = get_user_by_uid(session["uid"])
  return render_template('user/userinfo.html', user=user)
  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
