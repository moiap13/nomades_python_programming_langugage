import os
import csv

from flask import Flask, render_template, request

app = Flask(__name__)

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

        # TODO: insert data in csv database, hash the password using a salt
        # TODO: BONUS: check if email is already in csv file

        print(firstname, lastname, email, password, password_confirmation)
        return "Form sent successfully"
    else:
        return render_template("login/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email: str = ...
        password: str = ...

        # TODO: Open in "r" mode the users csv file using the constant CSV_FILE
        # TODO: Loop throught the lines and check if the current line is the user's one based on email
        # TODO: Check if password hashes match (don't forget to add the salt in the same way of the registration)
        # TODO: if login successful -> return "Login successful"
        # TODO: otw, return "Wrong credentials"
        return "Login successfully"
    else:
        return render_template("login/login.html")


# TODO: Add a new route for private part
# This route should be available only when someone is logged in
# Otw -> show message to login

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
