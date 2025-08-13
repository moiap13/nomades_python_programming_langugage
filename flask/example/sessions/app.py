import os
import csv
import hashlib
import random
import string

from flask import Flask, render_template, request, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "Some secret"

CURR_DIR: str = os.path.dirname(__file__)
CSV_FILE: str = os.path.join(CURR_DIR, "users.csv")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstname: str = request.form["tbx_firstname"]
        lastname: str = request.form["tbx_lastname"]
        email: str = request.form["tbx_email"]
        password: str = request.form["tbx_password"]
        password_confirmation: str = request.form["tbx_password_confirmation"]

        if (
            (
                not (
                    firstname
                    and lastname
                    and email
                    and password
                    and password_confirmation
                )
            )
            or ("@" not in email)
            or (password != password_confirmation)
        ):
            return "Please review the form"
        # BONUS: check if email is already in csv file
        with open(CSV_FILE, "r") as user_csv_file:
            csv_reader = csv.DictReader(user_csv_file)
            for row in csv_reader:
                if row.get("email").strip().lower() == email.strip().lower():
                    return "User already exists in database"

        # insert data in csv database
        with open(CSV_FILE, "a") as users_csv_file:
            # example using csv.writer
            # csv_writer = csv.writer(users_csv_file)
            # csv_writer.writerow([firstname, lastname, email, password])

            # example using dictwriter
            csv_writer = csv.DictWriter(
                users_csv_file,
                fieldnames=["firstname", "lastname", "email", "password", "salt"],
            )
            salt: str = "".join(random.choices(string.ascii_uppercase, k=10))
            h_pwd: str = hashlib.sha256((password + salt).encode()).hexdigest()
            csv_writer.writerow(
                {
                    "lastname": lastname,
                    "email": email,
                    "firstname": firstname,
                    "password": h_pwd,
                    "salt": salt,
                },
            )

        session["firstname"] = firstname
        session["lastname"] = lastname
        session["loggedin"] = True
        return "User successfully registered"
    else:
        return render_template("login/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email: str = request.form.get("tbx_email", "")
        password: str = request.form.get("tbx_password", "")

        if not (email and password) or "@" not in email:
            return "Please review the login form"

        # Open in "r" mode the users csv file using the constant CSV_FILE
        with open(CSV_FILE) as user_csv_file:
            csv_reader = csv.reader(user_csv_file)
            next(csv_reader)
            # Loop throught the lines of the csv file
            for row in csv_reader:
                if row[2].strip().lower() == email.strip().lower():
                    h_pwd: str = hashlib.sha256(
                        (password + row[4]).encode()
                    ).hexdigest()
                    if row[3] == h_pwd:
                        session["firstname"] = row[0]
                        session["lastname"] = row[1]
                        session["loggedin"] = True
                        return "Login successfully"
                    else:
                        return "Wrong credentials"
            return "User not in database"
    else:
        return render_template("login/login.html")


@app.route("/private")
def private():
    if "loggedin" in session and session["loggedin"]:
        return "This route is private !!"
    else:
        return 'Private zone please <a href="/login">login</a>'


@app.route("/show/session")
def show_session():
    return f"{session['firstname']}  {session['lastname']} {session['loggedin']}"


@app.route("/count")
def count():
    if "count" in session:
        session["count"] += 1
    else:
        session["count"] = 1
    return f"Count: {session['count']}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
