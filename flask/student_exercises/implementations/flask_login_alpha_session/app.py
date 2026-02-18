import os
import csv
import hashlib

import pandas as pd
from flask import Flask, render_template, request

from helpers.random_password_generator import generate_password as generate_salt

app = Flask(__name__)

CURR_DIR: str = os.path.dirname(__file__)
CSV_FILE: str = os.path.join(CURR_DIR, "users.csv")


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

        # Validation
        if not username or not pwd or not pwd2:
            return "Error: Please fill out the full formular"

        # Validate that the two passwords are the same
        if pwd != pwd2:
            # if different return "Password mismatch"
            return "Error: Passwords mismatch"

        if get_user_by_username(username):
            return f"Error: User with username={username} already exists"

        salt: str = generate_salt(True, False, False, False, 10)
        h_pwd: str = hashlib.sha256((pwd + salt).encode()).hexdigest()

        # Open in "a" mode the users csv file using the constant CSV_FILE
        with open(CSV_FILE, "a") as users_csv:
            writer = csv.writer(users_csv)
            # Add the new user to the CSV file
            writer.writerow([username, salt, h_pwd])

        return "User successfully registered"

        # TODO(BONUS): Check if user already exists in csv file, if so -> return "User already exists"
        return f""
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

        # Open in "r" mode the users csv file using the constant CSV_FILE
        # with open(CSV_FILE) as users_csv:
        #     reader = csv.DictReader(users_csv)
        #     # Loop throught the lines and check if the current line is the user's one
        #     for user in reader:
        #         # Check if password match, between users.csv password and the user's form password
        #         if user["uid"] == uid:
        #             # if login successful -> return "Login successful"
        #             salt: str = user["salt"]
        #             h_pwd: str = hashlib.sha256((pwd + salt).encode()).hexdigest()
        #             if user["pwd"] == h_pwd:
        #                 return "Login successfull"
        #             break

        user = get_user_by_username(uid)
        if user:
            salt: str = user["salt"]
            h_pwd: str = hashlib.sha256((pwd + salt).encode()).hexdigest()
            if user["pwd"] == h_pwd:
                return "Login successfull"

        # otw, return "Wrong credentials"
        return "Wrong credentials"

    else:
        return render_template("login/login.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
