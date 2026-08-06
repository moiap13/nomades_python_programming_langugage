import os
import hashlib

# import pandas as pd
from flask import Flask, render_template, request

from repositories.users_repository import get_user_by_uid, add_user

app = Flask(__name__)

CURR_DIR: str = os.path.dirname(__file__)
CSV_FILE: str = os.path.join(CURR_DIR, "users.csv")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET"])
def register_get():
    """
    Register function should add a new user to the users.csv file
    """
    return render_template("login/register.html")


@app.route("/register", methods=["POST"])
def register_post():
    """
    Register function should add a new user to the users.csv file
    """
    # get the user uid from form
    uid: str = request.form.get("uid", "").strip()
    # get the user password from form
    pwd: str = request.form.get("pwd", "").strip()
    # get the user password 2 from form
    pwd2: str = request.form.get("pwd2", "").strip()

    # validate that all the informations are sets
    if uid == '' or not pwd or not pwd2:
        return "Error: Please fill all the form's fields"
        
    # Validate that the two passwords are the same
    # if different return "Password mismatch"
    if pwd != pwd2:
        return "Error: Passwords mismatch"

    # (BONUS): Check if user already exists in csv file, if so -> return "User already exists"
    if get_user_by_uid(uid) != {}:
        return f"Error: User with uid={uid} already exists"

    # Open in "a" mode the users csv file using the constant CSV_FILE
    add_user(uid, pwd)
    
    return "User successfully registered"

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    The login functiojn should authenticate a user using his uid and pwd
    """
    if request.method == "POST":
        uid: str = request.form["uid"]
        pwd: str = request.form["pwd"]

        user: dict[str, str] = get_user_by_uid(uid)
        if user:
            h_pwd: str = hashlib.sha256((pwd+user["salt"]).encode()).hexdigest()
            if user["pwd"] == h_pwd:
                  # if login successful -> return "Login successful"
                  return "Login successfull"
        return "Wrong credentials"
        
    return render_template("login/login.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
