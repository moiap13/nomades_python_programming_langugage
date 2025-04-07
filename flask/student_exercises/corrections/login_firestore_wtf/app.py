import os
import csv
import json
from datetime import datetime
import hashlib

CURR_DIR = os.path.dirname(__file__)
CSV_FILE_PATH = os.path.join(CURR_DIR, "users.csv")
CONFIG_FILE_PATH = os.path.join(CURR_DIR, "server-creds.json")
CONFIG_FIRESTORE_PATH = os.path.join(CURR_DIR, "firestore-creds.json")

from flask import Flask, render_template, request, session, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.firestore import DocumentSnapshot

from helpers.random_password_generator import generate_password as generate_salt
from forms.login import LoginForm, RegisterForm

cred = credentials.Certificate(CONFIG_FIRESTORE_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()
print(db)

with open(CONFIG_FILE_PATH, "r") as json_config:
  config = json.load(json_config)
  
app = Flask(__name__)
app.config["SECRET_KEY"] = config["SECRET_KEY"]

@app.route("/signin", methods=["GET", "POST"])
def login():
  form = LoginForm(request.form)
  if request.method == "POST" and form.validate():
    email: str = form.email.data
    pwd: str = form.pwd.data

    # Read csv file to get the list of users
    # login using firestore
    #  - Loop throught all the users and check email password (/!\ hash password and salt)    

    # create a query to select the user with the email provided
    # the result should be 0 or 1
    # if 0 flash("Invalid credentials", "danger") -> return redirect login
    # if 1 get the user's DocumentSnapshot at index 0 and validate login using salt and password checking
  
    user = db.collection("users").where("email", "==", email).get()

    if len(user) != 1:
      flash("Wrong credentials", "danger")
      return render_template("login_wtf/login.html", form=form)

    user: DocumentSnapshot = user[0]
    user_data: dict[str, str | datetime] = user.to_dict()
    if "email" not in user_data or "password" not in user_data:
      flash("Error system please contact Antonio", "danger")
      return render_template("login_wtf/login.html", form=form)

    pwd_h: str = hashlib.sha256((pwd+user_data.get("salt", "")).encode()).hexdigest()
    if user_data["password"] == pwd_h:
      session["loggedin"] = True
      session["user"] = user_data
      session["uid"] = user.id
      flash("Login successful", "success")
      return redirect(url_for('userinfo'))

    flash("login unsucessful", "danger")
  return render_template("login_wtf/login.html", form=form)

@app.route("/signup", methods=["GET", "POST"])
def register():
  form = RegisterForm(request.form)

  # check if we are comming from GET or POST method
  if request.method == "POST" and form.validate():
    # If method == "POST", we want to insert the user in the csv file
    # accept the new input values
    # - Firstname
    # - lastname
    # - Username
    # - DoB
    # - Gender
    firstname: str = form.firstname.data
    lastname: str = form.lastname.data
    username: str = form.username.data
    dob: str =  datetime.strptime(form.dob.data.strftime("%Y-%m-%d"), "%Y-%m-%d")
    gender: str = form.gender.data
    email: str = form.email.data
    pwd: str = form.pwd.data

    # BONUS: before inserting new user check if eamil already exists in database
    # Same as login, don't loop throught the whole database
    # Query the user that has the email, two posssibilities 0 or 1
    # If 1 -> problem flash("Email already in use", "danger") -> return 
    # If 0 no problems
    user: list[DocumentSnapshot] = db.collection("users").where("email", "==", email).get()

    if len(user) == 1:
      flash("Email already in use", "danger")
      return render_template("login_wtf/register.html", form=form)

    # 2. Insert the email and password in the csv file
    #Insert user in database using `add()` function
    
    salt: str = generate_salt(True, False, False, False, 10, True)
    pwd_h: str = hashlib.sha256((pwd+salt).encode()).hexdigest()

    user: dict[str, str | datetime] = {
      "firstname": firstname,
      "lastname": lastname,
      "username": username,
      "date_of_birth": dob,
      "gender": gender,
      "email": email,
      "password": pwd_h,
      "salt": salt
    }

    _, docRef = db.collection("users").add(user)

    # 3. return "Register successful"
    # add the user infos to the session
    session["loggedin"] = True
    session["user"] = user
    session["uid"] = docRef.id
    flash("Registration successful", "success")
    return redirect(url_for('userinfo'))
  
  # IF method == "GET" return render template
  return render_template("login_wtf/register.html", form=form)

@app.route("/logout")
def logout():
  session.clear()
  flash("logout successful", "success")
  return redirect(url_for("login"))

@app.route("/userinfo")
def userinfo():
  # if not ("loggedin" in session and session["loggedin"]):
  if not session.get("loggedin", False):
    flash("Please login first", "warning")
    return redirect(url_for("login"))

  # Get the user infos from the session and pass them to the template
  return render_template("user/user_info.html", user=session["user"])

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8081, debug=True)