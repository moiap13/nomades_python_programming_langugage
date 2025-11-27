import os
import csv
from hashlib import sha256

import pandas as pd
from flask import Flask, render_template, request

from helpers.csv_funcs import get_user_by_uid
from helpers.password_generator import generate_password as generate_salt

app = Flask(__name__)

CURR_DIR: str = os.path.dirname(__file__)
CSV_FILE: str = os.path.join(CURR_DIR, "users.csv")


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

        # 2. Validate
        # Validate that the two passwords are the same
        if uid == "" or pwd == "" or pwd2 == "":
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
            writer.writerow([uid, h_pwd, salt])

        return f"User created successfully !"
    else:
        # GET
        return render_template("login/register.html")


@app.route("/login", methods=["GET", "POST"])
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
        user: dict[str, str] | None = get_user_by_uid(uid, CSV_FILE)
        if user:
            salt: str = user.get("salt", "")
            h_pwd: str = sha256((pwd + salt).encode()).hexdigest()
            if user["pwd"] == h_pwd:
                # if login successful -> return "Login successful"
                return "Login Successful"

        # otw, return "Wrong credentials"
        return "Wrong Credentials"
    else:
        return render_template("login/login.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
