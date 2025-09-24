import os
import hashlib
import random
import string
import uuid
import sys

from flask import Blueprint, request, flash, render_template, redirect, url_for, session

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
FIRESTORE_CREDS = os.path.join(ROOT_DIR, "configs", "firestore-creds.json")
UPLOAD_DIR: str = os.path.join(ROOT_DIR, "static", "uploads")

sys.path.append(ROOT_DIR)

from schema.user import User
from configs.firestore_connector import db, DocumentSnapshot


login_bp = Blueprint("login", __name__, url_prefix="/")


@login_bp.route("/register", methods=["GET", "POST"])
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
            return redirect(url_for("login.register"))

        salt: str = "".join(random.choices(string.ascii_uppercase, k=5))
        h_pwd: str = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
        pp_ext: str = pp.filename.split(".")[-1]
        pp_filename: str = f"{uuid.uuid4()}.{pp_ext}"
        pp.save(os.path.join(UPLOAD_DIR, pp_filename))

        # insert data in firestore database, using the firestore automatic id generator

        user_to_add: User = User(
            "", firstname, lastname, email, h_pwd, salt, pp_filename
        )
        _, doc_ref = db.collection("users").add(user_to_add.to_dict())

        session["loggedin"] = True
        session["uid"] = doc_ref.id
        flash("User successfully registered", "success")
        return redirect(url_for("userinfo"))
    else:
        return render_template("login/register.html")


@login_bp.route("/login", methods=["GET", "POST"])
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
            return redirect(url_for("login.login"))

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
            return redirect(url_for("userinfo"))

        flash("Wrong credentials", "danger")
        return redirect(url_for("login.login"))
    else:
        return render_template("login/login.html")


@login_bp.route("/logout")
def logout():
    if not (session.get("loggedin", False)):
        flash("Please login first", "warning")
        return redirect(url_for("login.login"))

    session["loggedin"] = False
    del session["loggedin"]
    # session.pop("loggedin")
    session.clear()

    flash("User successfully logged out", "success")
    return redirect(url_for("login.login"))
