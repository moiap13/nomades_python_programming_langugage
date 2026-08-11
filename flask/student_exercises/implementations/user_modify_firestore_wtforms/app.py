import os
import hashlib
import json
from uuid import uuid4

# import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.firestore import DocumentReference, DocumentSnapshot

from forms.login import LoginForm, RegisterForm
from helpers.decorators import authenticated
from exceptions.user import UserNotFoundError
from repositories.users_repository_firestore import get_user_by_email, get_user_by_uid, add_user, get_user_by_firestore_id, update_user

app = Flask(__name__)

CURR_DIR: str = os.path.dirname(__file__)
CREDS_FILE: str = os.path.join(CURR_DIR, "config", "creds.json")
FIREBASE_JSON: str = os.path.join(CURR_DIR, "config", "firestore-creds.json")
UPLOAD_FOLDER: str = os.path.join(CURR_DIR, "static", "uploads")

with open(CREDS_FILE) as config_file:
  config: dict[str, str] = json.load(config_file)

app.config["SECRET_KEY"] = config["secret_key"]

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
    form = RegisterForm(request.form)
    return render_template("login/register.html", form_values={}, form=form)


# TODO: Handle missing profile picture
@app.route("/signup", methods=["POST"])
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
    pp: "FileStorage" = form.pp.data

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
    pp_ext = pp.filename.split('.')[-1]
    pp_filename = f'{uuid4()}.{pp_ext}'
    pp.save(os.path.join(UPLOAD_FOLDER, pp_filename))

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
        "pp_filename": pp_filename
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
    form = LoginForm(request.form)

    if request.method == "POST" and form.validate():
        uid_email: str = form.uid.data
        pwd: str = form.pwd.data

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

        flash("Wrong credentials", "danger")
    return render_template("login/login.html", form=form)

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
# TODO: Update user modify to user WTForms
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
        # TODO: Handle file update in the update function
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
