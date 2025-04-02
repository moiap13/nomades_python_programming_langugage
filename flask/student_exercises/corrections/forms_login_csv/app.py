import os
import csv

from flask import Flask, render_template, request

app = Flask(__name__)

CURR_DIR = os.path.dirname(__file__)
CSV_FILE_PATH = os.path.join(CURR_DIR, "users.csv")

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    print(request.form)
    email: str = request.form.get("tbx_email")
    pwd: str = request.form.get("tbx_pwd")

    # TODO: Read csv file to get the list of users
    # TODO: for each user check if the login match the current user
    # TODO: if login match return "Login Successful" otw "Logi Unsuccessful"

    if email == "antonio@test.com" and pwd == "1234567890":
      return "Login Successful"
    else:
      return "Login Unsuccessful"
  else:
    return render_template("login/login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
  # TODO: check if we are comming from GET or POST method
  # IF method == "GET" return render template
  # If method == "POST", we want to insert the user in the csv file
    # 1. Check if both password match if no -> return "Password doesn't match"
    # 2. Insert the email and password in the csv file
    # 3. return "Register successful"
    # BONUS: before inserting new user check if eamil already exists in csv
      # if email already exists return "Email already in csv file"
  return render_template("login/register.html")

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8081, debug=True)