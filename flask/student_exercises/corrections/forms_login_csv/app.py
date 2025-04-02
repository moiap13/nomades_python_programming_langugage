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
    with open(CSV_FILE_PATH, "r") as csv_file:
      reader = csv.DictReader(csv_file)
      for row in reader:
        # TODO: for each user check if the login match the current user
        if email == row["email"] and pwd == row["password"]:
          # TODO: if login match return "Login Successful" otw "Logi Unsuccessful"
          return "Login Successful" 
    return "Login Unsuccessful"
  
  return render_template("login/login.html")

@app.route("/register", methods=["GET", "POST"])
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
    return "Register successful"
  

  # IF method == "GET" return render template
  return render_template("login/register.html")

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8081, debug=True)