import os
import json
import hashlib
import random
import string

from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash,
)

import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.firestore import DocumentReference, DocumentSnapshot

from schema.user import User

CURR_DIR: str = os.path.dirname(__file__)
CONFIG_FILE: str = os.path.join(CURR_DIR, "configs", "config_creds.json")
FIRESTORE_CREDS = os.path.join(CURR_DIR, "configs", "firestore-creds.json")
UPLOAD_DIR: str = os.path.join(CURR_DIR, "static", "uploads")

cred = credentials.Certificate(FIRESTORE_CREDS)
firebase_admin.initialize_app(cred)
db = firestore.client()
print(db)


class UserNotFound(Exception):
    pass


with open(CONFIG_FILE) as json_config:
    config: dict[str, str] = json.load(json_config)

app = Flask(__name__)
app.config["SECRET_KEY"] = config["secret_key"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get the data from form
        firstname: str = request.form.get("tbx_firstname", "").strip()
        lastname: str = request.form.get("tbx_lastname", "").strip()
        email: str = request.form.get("tbx_email", "").strip()
        password: str = request.form.get("tbx_password", "").strip()
        password_confirmation: str = request.form.get(
            "tbx_password_confirmation", ""
        ).strip()
        pp = request.files.get("pp_file")

        # Validate the form
        if (
            not (firstname or lastname and email and password and password_confirmation)
            or "@" not in email
            or password != password_confirmation
            or not pp
        ):
            flash("Error in formular, please review it", "danger")
            return render_template("login/register.html")

        # BONUS: check if email is already in csv file
        users_snapshot: list[DocumentSnapshot] = (
            db.collection("users").where("email", "==", email).get()
        )
        if len(users_snapshot) > 0:
            flash("User already exists, please login", "danger")
            return redirect(url_for("register"))

        salt: str = "".join(random.choices(string.ascii_uppercase, k=5))
        h_pwd: str = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
        pp.save(os.path.join(UPLOAD_DIR, pp.filename))

        # insert data in firestore database, using the firestore automatic id generator

        user_to_add: User = User(
            "", firstname, lastname, email, h_pwd, salt, pp.filename
        )
        _, doc_ref = db.collection("users").add(user_to_add.to_dict())

        session["loggedin"] = True
        session["uid"] = doc_ref.id
        flash("User successfully registered", "success")
        return redirect(url_for("private"))
    else:
        return render_template("login/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email: str = request.form.get("tbx_email", "").strip()
        password: str = request.form.get("tbx_password", "").strip()

        # adapt to use firestore queries instead of python for loops
        users_snapshot: list[DocumentSnapshot] = (
            db.collection("users").where("email", "==", email).get()
        )

        if len(users_snapshot) == 0:
            flash("Wrong credentials", "danger")
            return redirect(url_for("login"))

        assert len(users_snapshot) == 1, f"Many users matched email: {email}"
        user_dict: dict[str, str] = users_snapshot[0].to_dict()
        user_dict["uid"] = users_snapshot[0].id
        user: User = User.from_dict(user_dict)

        h_pwd: str = hashlib.sha256((password + user.salt).encode()).hexdigest()
        # Check if password hashes match (don't forget to add the salt in the same way of the registration)
        if user.password == h_pwd:
            # if login successful -> return "Login successful"
            session["loggedin"] = True
            session["uid"] = user.uid
            flash("Login successfull", "success")
            return redirect(url_for("private"))

        flash("Wrong credentials", "danger")
        return redirect(url_for("login"))
    else:
        return render_template("login/login.html")


@app.route("/logout")
def logout():
    if not (session.get("loggedin", False)):
        flash("Please login first", "warning")
        return redirect(url_for("login"))

    session["loggedin"] = False
    del session["loggedin"]
    # session.pop("loggedin")
    session.clear()

    flash("User successfully logged out", "success")
    return redirect(url_for("login"))


# Add a new route for private part
# This route should be available only when someone is logged in,
# this page display the infomration for the connected user
# (firstname, lastname, email)
# Otw -> redirect to login
@app.route("/private")
def private() -> str:
    # if not ("loggedin" in session and session["loggedin"]):
    if not (session.get("loggedin", False)):
        flash("Please login first", "warning")
        return redirect(url_for("login"))

    # Display user info (firstname, lastname, email) in the web page private.html
    user_snapshot: DocumentSnapshot = (
        db.collection("users").document(session["uid"]).get()
    )
    user: User = User.from_dict(user_snapshot.to_dict() | {"uid": user_snapshot.id})

    return render_template(
        "private.html",
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        pp_filename=os.path.join("uploads", user.pp_filename),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
