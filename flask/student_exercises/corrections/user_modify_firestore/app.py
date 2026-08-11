import os
import hashlib
import json

# import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.firestore import DocumentReference, DocumentSnapshot

from helpers.decorators import authenticated
from exceptions.user import UserNotFoundError
from repositories.users_repository_firestore import get_user_by_email, get_user_by_uid, add_user, get_user_by_firestore_id, update_user

app = Flask(__name__)

CURR_DIR: str = os.path.dirname(__file__)
CREDS_FILE: str = os.path.join(CURR_DIR, "config", "creds.json")
FIREBASE_JSON: str = os.path.join(CURR_DIR, "config", "firestore-creds.json")

with open(CREDS_FILE) as config_file:
  config: dict[str, str] = json.load(config_file)

app.config["SECRET_KEY"] = config["secret_key"]

CURR_DIR: str = os.path.dirname(__file__)
CSV_FILE: str = os.path.join(CURR_DIR, "users.csv")

cred = credentials.Certificate(FIREBASE_JSON)
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
    if get_user_by_uid(db, uid) != {}:
        return render_template("login/register.html", error=f"Error: User with uid={uid} already exists", form_values=request.form)

    if get_user_by_email(db, email) != {}:
        return render_template("login/register.html", error=f"Error: User with email={email} already exists", form_values=request.form)

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

    user_added: dict[str, str] = add_user(db, user_dict)
    session["loggedin"] = True
    session["uid"] = uid
    session["firestore_id"] = user_added.get("firestore_id", "")
    # session["user"] = user_dict
    
    flash("User successfully registered", "success")
    return redirect(url_for("user_info"))

@app.route("/signin", methods=["GET", "POST"])
def login():
    """
    The login functiojn should authenticate a user using his uid and pwd
    """
    if request.method == "POST":
        uid_email: str = request.form["uid_email"]
        pwd: str = request.form["pwd"]

        try:
            user: dict[str, str] = get_user_by_uid(db, uid_email)
        except UserNotFoundError:
            try: 
                user: dict[str, str] = get_user_by_email(db, uid_email)
            except UserNotFoundError:
                return "Wrong credentials"
                            
        h_pwd: str = hashlib.sha256((pwd+user["salt"]).encode()).hexdigest()
        if user["pwd"] == h_pwd:
            # if login successful -> return "Login successful"
            session["loggedin"] = True
            session["uid"] = uid_email
            session["firestore_id"] = user.get("firestore_id", "")
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
def user_info() -> str:
  # user: dict[str, str] = get_user_by_uid(db, session["uid"])
  try:
      user: dict[str, str] = get_user_by_firestore_id(db, session["firestore_id"])
  except ValueError:
      user: dict[str, str] = get_user_by_firestore_id(db, str(session["firestore_id"]))
  except UserNotFoundError:
      return redirect(url_for("logout"))
  
  return render_template('user/userinfo.html', user=user)
  
# this route accept both get and post requests
# This route should be private (not public, meaning secured by authentication)
@app.route("/user/modify", methods=["GET", "POST"])
@authenticated
def user_modify() -> str:
    user: dict[str, str] = get_user_by_firestore_id(db, session["firestore_id"])

    if request.method == "POST":
        # POST: 
        #  1. get all the values from the form
        firstname: str = request.form.get("firstname", "").strip()
        lastname: str = request.form.get("lastname", "").strip()
        email: str = request.form.get("email", "").strip()
        uid: str = request.form.get("uid", "").strip()

        #  2. Validate the update form (no null values, check uniqueness of uid and email)
        if not firstname or not lastname or not email or not uid:
            flash("Please fill all the form's fields", "danger")
            return render_template("user/usermodify.html", user=request.form)

        if email != user["email"]:
          try:
            get_user_by_email(db, email)
          except UserNotFoundError: 
              pass
          else:
              flash(f"User with email={email} already exists", "danger")
              return render_template("user/usermodify.html", user=request.form)

        if uid != user["uid"]:
          try:
            get_user_by_uid(db, uid)
            flash(f"User with uid={uid} already exists", "danger")
            return render_template("user/usermodify.html", user=request.form)
          except UserNotFoundError: 
              pass
        
        #  3. Update the database document for the logged user (use the update function from the firestore repo)
        update_user(db, session["firestore_id"], {
            "firstname": firstname, 
            "lastname": lastname, 
            "email": email, 
            "uid": uid
        })

        #  4. redirect to /user/info route
        flash("User successfully updated", "success")
        return redirect(url_for("user_info"))

            
    # GET -> render_template user/usermodify.html
    return render_template("user/usermodify.html", user=user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
