import os
import csv
import json

from flask import Flask, render_template, request, session, redirect, url_for

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

    # TODO: Read csv file to get the list of users
    with open(CSV_FILE_PATH, "r") as csv_file:
      reader = csv.DictReader(csv_file)
      for row in reader:
        # TODO: for each user check if the login match the current user
        if email == row["email"] and pwd == row["password"]:
          # TODO: if login match return "Login Successful" otw "Logi Unsuccessful"
          session["loggedin"] = True
          return redirect(url_for('private'))
    return "Login Unsuccessful"
  
  return render_template("login/login.html")

@app.route("/signup", methods=["GET", "POST"])
def register():
  # TODO: check if we are comming from GET or POST method
  if request.method == "POST":
    # If method == "POST", we want to insert the user in the csv file
    email: str = request.form.get("tbx_email")
    pwd: str = request.form.get("tbx_pwd")
    pwd_repeat: str = request.form.get("tbx_pwd_repeat")

    # 1. Check if both password match if no -> return "Password doesn't match"
    if pwd != pwd_repeat:
      return "Password mismatch"

    # BONUS: before inserting new user check if eamil already exists in csv
    with open(CSV_FILE_PATH, "r") as csv_file:
      reader = csv.reader(csv_file)
      next(reader)
      for row in reader:
        if row[0] == email:
          # if email already exists return "Email already in csv file"
          return "Email already in csv file"

    # 2. Insert the email and password in the csv file
    with open(CSV_FILE_PATH, mode="a") as csv_file:
      csv_writer = csv.writer(csv_file)
      csv_writer.writerow([email, pwd])

    # 3. return "Register successful"
    session["loggedin"] = True
    return redirect(url_for('private'))
  

  # IF method == "GET" return render template
  return render_template("login/register.html")

@app.route("/logout")
def logout():
  session.clear()
  return redirect(url_for("login"))

@app.route("/private")
def private():
  # if not ("loggedin" in session and session["loggedin"]):
  if not session.get("loggedin", False):
    return "Please login first"
  
  return render_template("user/user_info.html")

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8081, debug=True)