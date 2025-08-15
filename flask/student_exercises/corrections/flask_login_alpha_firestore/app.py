import hashlib
import os
import csv
import random
import string

from flask import Flask, render_template, request, session, redirect, flash
import firebase_admin
from firebase_admin import credentials, firestore

CURR_DIR: str = os.path.dirname(__file__)
FIRESTORE_KEY_PATH: str = os.path.join(CURR_DIR, "firestore-creds.json")

app = Flask(__name__)
app.config["SECRET_KEY"] = "Some secret !"

cred = credentials.Certificate(FIRESTORE_KEY_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()
print(db)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstname: str = request.form["tbx_firstname"]
        lastname: str = request.form["tbx_lastname"]
        email: str = request.form["tbx_email"]
        password: str = request.form["tbx_password"]
        password_confirmation: str = request.form["tbx_password_confirmation"]

        if (
            (
                not (
                    firstname
                    and lastname
                    and email
                    and password
                    and password_confirmation
                )
            )
            or ("@" not in email)
            or (password != password_confirmation)
        ):
            return "Please review the form"

        for user in db.collection("users").stream():
            user_data: dict[str, str] = user.to_dict()
            if user_data.get("email").strip().lower() == email.strip().lower():
                flash("Email alreeady in use", "danger")
                return redirect("/register")
        # TODO: insert data in firestore database
        # insert the user dictionnary (see below) in the "users" collection

        salt: str = "".join(random.choices(string.ascii_uppercase, k=10))
        h_pwd: str = hashlib.sha256((password + salt).encode()).hexdigest()
        user: dict[str, str] = {
            "lastname": lastname,
            "email": email,
            "firstname": firstname,
            "password": h_pwd,
            "salt": salt,
        }
        _, doc = db.collection("users").add(user)
        print(f"User successfully registered with id {doc.id}")

        session["firstname"] = firstname
        session["lastname"] = lastname
        session["email"] = email
        session["loggedin"] = True
        flash("User successfully registered", "success")
        return redirect("/home")
    else:
        return render_template("login/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email: str = request.form.get("tbx_email", "")
        password: str = request.form.get("tbx_password", "")

        if not (email and password) or "@" not in email:
            flash("Please review the login form", "danger")
            return redirect("/login")

        # Check if user exists in database and check if email/password matchd
        # Loop throught all the documents from the usesrs collection
        for user in db.collection("users").stream():
            user_data: dict[str, str] = user.to_dict()
            if user_data.get("email").strip().lower() == email.strip().lower():
                salt: str = user_data.get("salt")
                h_pwd: str = hashlib.sha256(
                    (password + salt).encode(encoding="utf-8")
                ).hexdigest()
                if user_data.get("password") == h_pwd:
                    session["firstname"] = user_data.get("firstname")
                    session["lastname"] = user_data.get("lastname")
                    session["email"] = user_data.get("email")
                    session["loggedin"] = True
                    flash("Logged in successfully", "success")
                    return redirect("/home")
                else:
                    flash("Wrong credentials", "danger")
                    return redirect("/login")
            flash("User not in database", "danger")
            return redirect("/login")
    else:
        return render_template("login/login.html")


@app.route("/logout")
def logout():
    session["loggedin"] = False
    session.pop("loggedin")
    session.clear()
    flash("Successfully logged out", "success")
    return redirect("/login")


# Add a new route for private part
# This route should be available only when someone is logged in
# Otw -> show message to login
@app.route("/private")
def private():
    if "loggedin" in session and session["loggedin"]:
        return "Private part !"
    else:
        return redirect("/login")


@app.route("/home")
def home():
    if not ("loggedin" in session and session["loggedin"]):
        flash("Login first", "warning")
        return redirect("/login")

    return render_template(
        "user/home.html",
        firstname=session["firstname"],
        lastname=session["lastname"],
        email=session["email"],
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
