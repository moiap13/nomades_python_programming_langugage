import os
import json
from hashlib import sha256
import csv

from flask import Flask, render_template, request, session, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.firestore import DocumentReference, DocumentSnapshot

from helpers.errors import UserNotFoundError
from helpers.firestore_funcs import get_user_by_uid
from helpers.password_generator import generate_password as generate_salt
from helpers.decorators import authenticated

CURR_DIR: str = os.path.dirname(__file__)
CSV_FILE: str = os.path.join(CURR_DIR, "users.csv")
CONFIG: str = os.path.join(CURR_DIR, "config", "creds.json")
FIREBASE_JSON: str = os.path.join(CURR_DIR, "config", "firestore-creds.json")

cred = credentials.Certificate(FIREBASE_JSON)
firebase_admin.initialize_app(cred)
db = firestore.client()
print(db)

with open(CONFIG) as json_config:
    config: dict[str, str] = json.load(json_config)

app = Flask(__name__)
app.config["SECRET_KEY"] = config["secret_key"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register function should add a new user to the users.csv file
    """
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
        try:
            age: int = int(request.form.get("age", ""))
        except ValueError:
            flash("Age must be numeric", "danger")
            return render_template(
                "login/register.html",
                form_values={
                    "firstname": firstname,
                    "lastname": lastname,
                    "uid": uid,
                    "email": email,
                    "age": "0",
                },
            )

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
        # (BONUS): Check if user already exists by uid
        # TODO: Check if user already exists by email
        try:
            get_user_by_uid(uid, db)
        except UserNotFoundError:
            pass
        else:
            flash(f"User with uid={uid} already exists", "danger")
            return render_template(
                "login/register.html",
                form_values={
                    "firstname": firstname,
                    "lastname": lastname,
                    "uid": uid,
                    "email": email,
                    "age": age,
                },
            )

        # Add user to the database
        # Add the new user to the CSV file
        salt: str = generate_salt(True, False, False, False, 10)
        h_pwd: str = sha256((pwd + salt).encode()).hexdigest()
        _, doc_ref = db.collection("users").add(
            {
                "firstname": firstname,
                "lastname": lastname,
                "uid": uid,
                "email": email,
                "age": age,
                "salt": salt,
                "pwd": h_pwd,
            }
        )

        session["loggedin"] = True
        session["uid"] = uid
        session["firestore_id"] = doc_ref.id
        flash("User successfully created", "success")
        return redirect(url_for("user_info"))
    else:
        # GET
        return render_template("login/register.html", form_values={})


# TODO: Actually the login loops throught each users of the database, implement a query that gives the user by uid directly
@app.route("/signin", methods=["GET", "POST"])
def login():
    """
    The login functiojn should authenticate a user using his uid and pwd
    """
    if request.method == "POST":
        # 1. Get the datas
        uid: str = request.form["uid"]
        pwd: str = request.form["pwd"]

        # 2. Validate
        if uid == "" or pwd == "":
            return "Error: please fill the form"

        # 3. Logic
        # Open in "r" mode the users csv file using the constant CSV_FILE
        try:
            user: dict[str, str | int] = get_user_by_uid(uid, db)
        except UserNotFoundError:
            flash("Wrong credentials", "danger")
            return redirect(url_for("login"))

        salt: str = user.get("salt", "")
        h_pwd: str = sha256((pwd + salt).encode()).hexdigest()
        if user["pwd"] == h_pwd:
            # if login successful -> return "Login successful"
            session["loggedin"] = True
            session["uid"] = uid
            session["firestore_id"] = user.get("id", "")
            flash("Login successful", "success")
            return redirect(url_for("user_info"))

        # otw, return "Wrong credentials"
        flash("Wrong credentials", "danger")
        return redirect(url_for("login"))
    else:
        return render_template("login/login.html")


@app.route("/logout")
def logout():
    session["loggedin"] = False
    session.pop("loggedin")
    session.clear()
    flash("Logout successful", "success")

    return redirect(url_for("login"))


@app.route("/user/info")
@authenticated
def user_info() -> str:
    # try:
    #     user: dict[str, str] = get_user_by_uid(session["uid"], db)
    # except UserNotFoundError:
    #     flash("User not found", "danger")
    #     return redirect("logout")
    user: dict[str, str | int] = (
        db.collection("users").document(session["firestore_id"]).get().to_dict()
    )

    return render_template("user/userinfo.html", user=user)


# create the /user/modify route
# this route accepts GET and POST requests
# If GET request -> return the usermodify.html page (you need to create it)
# If POST reqeust -> get the datas and modify the user in the csv
# create the webpage user/usermodify.html
# check the value attribute for inputs


@app.route("/user/modify", methods=["GET", "POST"])
def user_modify():
    # TODO: Allow the user to modify bith email and uid
    # TODO: email and uid must be unique in database
    try:
        user: dict[str, str | int] = get_user_by_uid(session["uid"], db)
    except UserNotFoundError:
        flash("Error: user not found", "danger")
        return redirect(url_for("user_info"))

    if request.method == "POST":
        firstname: str = request.form.get("tbx_firstname")
        lastname: str = request.form.get("tbx_lastname")
        email: str = request.form.get("tbx_email")
        old_pwd: str = request.form.get("tbx_old_pwd")
        new_pwd: str = request.form.get("tbx_new_pwd")
        try:
            age: int = int(request.form.get("tbx_age"))
        except ValueError:
            flash("Age must be integer, value set to 0", "danger")
            age = 0

        if firstname == "" or lastname == "" or email == "" or age == "":
            flash("Please fill the inputs: Firstname, Lastname, Email, Age", "danger")
            return render_template("user/usermodify.html", user=user)

        if "@" not in email:
            flash("Please enter a valid email address", "danger")
            return render_template("user/usermodify.html", user=user)

        if (old_pwd != "" and new_pwd == "") or (old_pwd == "" and new_pwd != ""):
            flash("Please enter both old and new password fields", "danger")
            return render_template("user/usermodify.html", user=user)

        new_salt: str = ""
        h_new_pwd: str = ""
        if old_pwd != "" and new_pwd != "":
            h_old_pwd: str = sha256(
                (old_pwd + user.get("salt", "")).encode()
            ).hexdigest()
            if h_old_pwd != user["pwd"]:
                flash("Old password error", "danger")
                return render_template("user/usermodify.html", user=user)

            new_salt = generate_salt(True, False, False, False, 10)
            h_new_pwd = sha256((new_pwd + new_salt).encode()).hexdigest()

        user_doc_ref: DocumentReference = db.collection("users").document(
            session["firestore_id"]
        )
        user_doc_ref.update(
            {
                "firstname": firstname,
                "lastname": lastname,
                "email": email,
                "age": age,
                "uid": session["uid"],
                "pwd": h_new_pwd if h_new_pwd != "" else user["pwd"],
                "salt": new_salt if new_salt else user["salt"],
            }
        )

        flash("User updated successfully", "success")
        return redirect(url_for("user_modify"))

    return render_template("user/usermodify.html", user=user)


@app.route("/private")
@authenticated
def secret() -> str:
    return "Welcome to the private part"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
