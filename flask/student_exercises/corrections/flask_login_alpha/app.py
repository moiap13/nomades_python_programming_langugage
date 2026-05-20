import os
import csv
import hashlib

import pandas as pd
from flask import Flask, render_template, request

from helpers.random_password_generator import generate_password as generate_salt
from helpers.csv_database import get_user_by_uid

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

        # 2. Validate the data
        if (not uid  or not pwd or not pwd2):
          return "Error: Please fill out the form"

        if pwd != pwd2:
          # if different return "Password mismatch"
          return "Error: Password mismatch"

        # 3. buisness logic
        # (BONUS): Check if user already exists in csv file, if so -> return "User already exists"
        if get_user_by_uid(uid, CSV_FILE) != None:
          return "Error: User already exists"

        # Open in "a" mode the users csv file using the constant CSV_FILE
        with open(CSV_FILE, "a") as users_file:
          writer = csv.writer(users_file)
          # Add the new user to the CSV file
          salt: str = generate_salt(True, False, False, False, 10)
          pwd_h: str = hashlib.sha256((pwd+salt).encode()).hexdigest()
          writer.writerow([uid, pwd_h, salt])
        
        return "User successfully registered"
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
        user_row: dict[str, str] | None = get_user_by_uid(uid, CSV_FILE)
        if user_row != None:
          # Check if password match, between users.csv password and the user's form password
          salt: str = user_row.get("salt", "")
          pwd_h: str = hashlib.sha256((pwd+salt).encode()).hexdigest()
          if user_row.get("pwd") == pwd_h:
            # if login successful -> return "Login successful"
            return "Login successful"
          
        # otw, return "Wrong credentials"
        return "Wrong credentials"
    else:
        return render_template("login/login.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
