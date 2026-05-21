import os
import json
from hashlib import sha256
import csv

from flask import Flask, render_template, request, session, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from helpers.csv_funcs import get_user_by_uid
from helpers.password_generator import generate_password as generate_salt

CURR_DIR: str = os.path.dirname(__file__)
CSV_FILE: str = os.path.join(CURR_DIR, "users.csv")
FIRESTORE_CREDS: str = os.path.join(CURR_DIR, 'config', 'firestore-creds.json')

with open(os.path.join(CURR_DIR, "config", "creds.json")) as json_config:
    config: dict[str, str] = json.load(json_config)

app = Flask(__name__)
app.config["SECRET_KEY"] = config["secret_key"]

# Connection a firebase
cred = credentials.Certificate(FIRESTORE_CREDS)
firebase_admin.initialize_app(cred)# Connection a firestore
db = firestore.client()
print(db)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register function should add a new user to the users.csv file
    """
     # TODO: adapt the code to use firestore instead of csv
    if request.method == "POST":
        # 1. Get the data
        # get the user uid from form
        uid: str = request.form.get("uid", "")
        # get the user password from form
        pwd: str = request.form.get("pwd", "")
        # get the user password 2 from form
        pwd2: str = request.form.get("pwd2", "")
        firstname: str = request.form.get("firstname", "")
        lastname: str = request.form.get("lastname", "")
        email: str = request.form.get("email", "")
        age: str = request.form.get("age", "")

        # 2. Validate
        # Validate that the two passwords are the same
        if (
            uid == ""
            or pwd == ""
            or pwd2 == ""
            or firstname == ""
            or lastname == ""
            or email == ""
            or age == ""
        ):
            return "Error: please fill the form"
        if pwd != pwd2:
            return "Error: password mismatch"

        # 3. Logic
        # (BONUS): Check if user already exists in csv file, if so -> return "User already exists"
        if get_user_by_uid(uid, CSV_FILE) != None:
            return "User alreeady exists"

        # Open in "a" mode the users csv file using the constant CSV_FILE
        with open(CSV_FILE, "a") as users_file:
            writer = csv.writer(users_file)
            # Add the new user to the CSV file
            salt: str = generate_salt(True, False, False, False, 10)
            h_pwd: str = sha256((pwd + salt).encode()).hexdigest()
            writer.writerow([firstname, lastname, email, age, uid, h_pwd, salt])

        session["loggedin"] = True
        session["uid"] = uid

        flash(f"User {uid} successfully registered", "success")

        return redirect(url_for("user_info"))
    else:
        # GET
        return render_template("login/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    The login functiojn should authenticate a user using his uid and pwd
    """
    # TODO: adapt the code to use firestore instead of csv
    # TODO: For login, get all the documents from the collection and loop using python's for loop
    if request.method == "POST":
        # 1. Get the datas
        uid: str = request.form["uid"]
        pwd: str = request.form["pwd"]

        # 2. Validate
        if uid == "" or pwd == "":
            return "Error: please fill the form"

        # 3. Logic
        # Open in "r" mode the users csv file using the constant CSV_FILE
        user: dict[str, str] | None = get_user_by_uid(uid, CSV_FILE)
        if user:
            salt: str = user.get("salt", "")
            h_pwd: str = sha256((pwd + salt).encode()).hexdigest()
            if user["pwd"] == h_pwd:
                # if login successful -> return "Login successful"
                flash("Login successful", "success")
                session["loggedin"] = True
                session["uid"] = uid

                return redirect(url_for("user_info"))

        # otw, return "Wrong credentials"
        return "Wrong Credentials"
    else:
        return render_template("login/login.html")


@app.route("/logout")
def logout():
    # logout the user; think about session
    session["loggedin"] = False
    session.pop("loggedin")
    session.clear() 
    # redirect to login route
    flash("logout successful", "success")
    return redirect(url_for('login'))


@app.route("/user/info")
def user_info() -> str:
     # TODO: adapt the code to use firestore instead of csv
    # protect this route
    if not ("loggedin" in session and session["loggedin"] == True):
        # I'm not logged in !!
        flash("Please login first", "warning")
        return redirect(url_for('login'))

    assert(session["loggedin"] == True)
    # get the user informations (CSV or session as you want)
    user: dict[str, str] | None = get_user_by_uid(session["uid"], CSV_FILE)
    if user == None:
        return redirect(url_for('login'))
    
    assert(type(user) == dict)
    # pass the user to the userinfo.html file (read the htlm file to understand the type of the variable user)

    return render_template("user/userinfo.html", user=user) # pass the user



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
