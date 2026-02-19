import os
import csv
import hashlib
import json

import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for, flash

from helpers.random_password_generator import generate_password as generate_salt


CURR_DIR: str = os.path.dirname(__file__)
CSV_FILE: str = os.path.join(CURR_DIR, "users.csv")
CONFIG_FILE: str = os.path.join(CURR_DIR, "config", "creds.json")

with open(CONFIG_FILE) as config_file:
    config: dict[str, str] = json.load(config_file)

app = Flask(__name__)
app.secret_key = config["secret_key"]


def get_user_by_username(uid: str) -> dict[str, str] | None:
    with open(CSV_FILE) as users_csv:
        reader = csv.DictReader(users_csv)
        for user in reader:
            if user["uid"] == uid:
                return user


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["get", "post"])
def register():
    """
    Register function should add a new user to the users.csv file
    """
    if request.method == "POST":
        # get the user uid from form
        username: str = request.form["uid"]
        # get the user password from form
        pwd: str = request.form.get("pwd")
        # get the user password 2 from form
        pwd2: str = request.form.get("pwd2")
        # TODO: handle firstname, email, lastname, avatar data

        # Validation
        # TODO: check firstname, lastname, avatar can't be null
        if not username or not pwd or not pwd2:
            flash("Error: Please fill out the full formular", "danger")
            return redirect(url_for("register"))

        # Validate that the two passwords are the same
        if pwd != pwd2:
            # if different return "Password mismatch"
            flash("Error: Passwords mismatch", "danger")
            return redirect(url_for("register"))

        # TODO: check that avatar is from jpg, jpeg or png format
        # if not correct type -> flash please provide a valid image

        # TODO: validate email (check that @ char is present in string)
        # if not a correct email -> flash please provide a valid email

        if get_user_by_username(username):
            flash(f"Error: User with username={username} already exists", "danger")
            return redirect(url_for("register"))

        salt: str = generate_salt(True, False, False, False, 10)
        h_pwd: str = hashlib.sha256((pwd + salt).encode()).hexdigest()

        # Open in "a" mode the users csv file using the constant CSV_FILE
        with open(CSV_FILE, "a") as users_csv:
            writer = csv.writer(users_csv)
            # Add the new user to the CSV file
            # TODO: add the firstname, lastname and avaatr to the csv database
            writer.writerow([username, salt, h_pwd])

        session["loggedin"] = True
        session["uid"] = username
        flash("User successfully registered", "success")
        return redirect(url_for("private"))
    else:
        return render_template("login/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    The login functiojn should authenticate a user using his uid and pwd
    """
    if request.method == "POST":
        uid: str = request.form["uid"]
        pwd: str = request.form["pwd"]

        user = get_user_by_username(uid)
        if user:
            salt: str = user["salt"]
            h_pwd: str = hashlib.sha256((pwd + salt).encode()).hexdigest()
            if user["pwd"] == h_pwd:
                session["loggedin"] = True
                session["uid"] = uid
                flash("Login successfull", "success")
                return redirect(url_for("private"))

        # otw, return "Wrong credentials"
        flash("Wrong credentials", "danger")
        return redirect(url_for("login"))

    else:
        return render_template("login/login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("User logged out successfully", "success")
    return redirect(url_for("login"))


@app.route("/private")
def private():
    if not session.get("loggedin", False):
        flash("Please log in first", "warning")
        return redirect("/login")  # TODO: change for using url_for ;)

    return render_template("private/private.html")


# TODO: create a new private route to displays user informations
# The user infomrations will be the one given by the register:
# - Firstname
# - Lastname
# - Email
# - Username
# - Password
# - Avatar


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
