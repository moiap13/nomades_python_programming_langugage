import os
import json

from flask import Flask, render_template, request, session, redirect, url_for

from repository.user_csv import CSV_FILE, get_user_by_uid, add_user
from helpers.random_password_generator import generate_password as generate_salt
from helpers.security import hash_pwd

CURR_DIR: str = os.path.dirname(__file__)
CONFIG_DIR: str = os.path.join(CURR_DIR, "config")
CREDS_FILE: str = os.path.join(CONFIG_DIR, "creds.json")

with open(CREDS_FILE) as creds_json:
    config: dict[str, str] = json.load(creds_json)

app = Flask(__name__)
app.config["SECRET_KEY"] = config["secret_key"]

                  
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def register():
    """
    Register function should add a new user to the users.csv file
    """
    if request.method == "POST":
        # get the user uid from form
        # get the user password from form
        # get the user password 2 from form
        uid: str = request.form.get("uid", "")
        pwd: str = request.form.get("pwd", "")
        pwd2: str = request.form.get("pwd2", "")

        # Validate that the two passwords are the same
        # if different return "Password mismatch"
        if not uid or not pwd or not pwd2:
            return "Error: Please fill out all the forms fiels"

        if pwd != pwd2:
            return "Error: passwords mismatch"
        
        # (BONUS): Check if user already exists in csv file, if so -> return "User already exists"
        if get_user_by_uid(uid, CSV_FILE):
            return "Error: User already exists"
                
        # Open in "a" mode the users csv file using the constant CSV_FILE
        salt: str = generate_salt(True, False, False, False, 10)
        h_pwd: str = hash_pwd(pwd, salt)

        add_user({
            "uid": uid,
            "pwd": h_pwd,
            "salt": salt
        }, CSV_FILE)

        session["loggedin"] = True
        session["uid"] = uid
        
        return "User successfully registered"
    else:
        # GET
        return render_template("login/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    The login functiojn should authenticate a user using his uid and pwd
    """
    if request.method == "POST":
        uid: str = request.form.get("uid", "")
        pwd: str = request.form.get("pwd", "")

        if not uid or not pwd:
            return "Error: Please fill out the form"

        # Open in "r" mode the users csv file using the constant CSV_FILE
        user: dict[str, str] = get_user_by_uid(uid, CSV_FILE)
        if user:
            h_pwd: str = hash_pwd(pwd, user["salt"])
            if user["pwd"] == h_pwd:
              # if login successful -> return "Login successful"
              session["loggedin"] = True
              session["uid"] = uid

              # return "Login successful"
              return redirect(url_for("home"))
            
        return "Wrong credentials"
    else:
        return render_template("login/login.html")

@app.route("/home")
def home():
    if not session.get("loggedin", False):
        # return "Warning: Please login first"
        return redirect(url_for("login"))
     
    return render_template("user/userinfo.html", uid=session["uid"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
