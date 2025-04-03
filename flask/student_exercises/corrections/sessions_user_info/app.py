import os
import csv
import json
from datetime import datetime
import hashlib

from flask import Flask, render_template, request, session, redirect, url_for, flash

from helpers.random_password_generator import generate_password as generate_salt

CURR_DIR = os.path.dirname(__file__)
CSV_FILE_PATH = os.path.join(CURR_DIR, "users.csv")
CONFIG_FILE_PATH = os.path.join(CURR_DIR, "server-creds.json")

with open(CONFIG_FILE_PATH, "r") as json_config:
  config = json.load(json_config)
  
app = Flask(__name__)
app.config["SECRET_KEY"] = config["SECRET_KEY"]

@app.route("/signin", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    email: str = request.form.get("tbx_email")
    pwd: str = request.form.get("tbx_pwd")

    # Read csv file to get the list of users
    with open(CSV_FILE_PATH, "r") as csv_file:
      reader = csv.DictReader(csv_file)
      for row in reader:
        # for each user check if the login match the current user
        pwd_h: str = hashlib.sha256((pwd+row["salt"]).encode()).hexdigest()
        if email == row["email"] and pwd_h == row["password"]:
          # if login match return "Login Successful" otw "Logi Unsuccessful"
          session["loggedin"] = True
          session["user"] = {
            "firstname": row["firstname"],
            "lastname": row["lastname"],
            "email": row["email"],
            "username": row["username"],
            "date_of_birth": row["dob"],
            "gender": row["gender"],
          }
          flash("Login successful", "success")
          return redirect(url_for('userinfo'))
    flash("login unsucessful", "danger")

  return render_template("login/login.html")

@app.route("/signup", methods=["GET", "POST"])
def register():
  # check if we are comming from GET or POST method
  if request.method == "POST":
    print(request.form)
    # If method == "POST", we want to insert the user in the csv file
    # accept the new input values
    # - Firstname
    # - lastname
    # - Username
    # - DoB
    # - Gender
    firstname: str = request.form.get("tbx_firstname")
    lastname: str = request.form.get("tbx_lastname")
    username: str = request.form.get("tbx_username")
    dob: str = request.form.get("dp_dob")
    gender: str = request.form.get("r_gender")
    email: str = request.form.get("tbx_email")
    pwd: str = request.form.get("tbx_pwd")
    pwd_repeat: str = request.form.get("tbx_pwd_repeat")

    # 1. Check if both password match if no -> return "Password doesn't match"
    if pwd != pwd_repeat:
      flash("Password mismatch", "danger")
      return render_template("login/register.html")

    if (
      firstname == ""
      or lastname == ""
      or username == ""
      or dob == ""
      or gender == ""
      or email == ""
      or pwd == ""
      or pwd_repeat == ""
    ): 
      flash("Please fill all the fields", "danger")
      return render_template("login/register.html")

    date_of_birth: datetime = datetime.strptime(dob, "%Y-%m-%d")

    # BONUS: before inserting new user check if eamil already exists in csv
    with open(CSV_FILE_PATH, "r") as csv_file:
      reader = csv.reader(csv_file)
      next(reader)
      for row in reader:
        if row[5] == email:
          # if email already exists return "Email already in csv file"
          flash("Email already in csv file", "danger")
          return render_template("login/register.html")

    # 2. Insert the email and password in the csv file
    with open(CSV_FILE_PATH, mode="a") as csv_file:
      # write the user info in the csv file
      csv_writer = csv.writer(csv_file)
      salt: str = generate_salt(True, False, False, False, 10, True)
      pwd_h: str = hashlib.sha256((pwd+salt).encode()).hexdigest()
      csv_writer.writerow([firstname, lastname, username, date_of_birth.strftime("%Y-%m-%d"), gender, email, pwd_h, salt])

    # 3. return "Register successful"
    # add the user infos to the session
    session["loggedin"] = True
    session["user"] = {
      "firstname": firstname,
      "lastname": lastname,
      "username": username,
      "date_of_birth": date_of_birth.strftime("%Y-%m-%d"),
      "gender": gender,
      "email": email
    }
    flash("Registration successful", "success")
    return redirect(url_for('userinfo'))
  
  # IF method == "GET" return render template
  return render_template("login/register.html")

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