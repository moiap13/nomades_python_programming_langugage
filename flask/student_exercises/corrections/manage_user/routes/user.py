# Create the user blueprint file, where the name of the blueprint is user and the url prefix is /user
# this file will contain two routes the route for /user/info and the route for /user/modify
# DO not forget to register the blueprint in the app instance

import os
import sys

from flask import Blueprint, session, flash, redirect, url_for, render_template, request

ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from configs.firestore_connector import db, DocumentSnapshot
from helpers.decorators import authenticated
from schema.user import User

user_bp = Blueprint("user", __name__, url_prefix="/user")


# move this route to the user blueprint
@user_bp.route("/info")
@authenticated
def userinfo() -> str:
    # Display user info (firstname, lastname, email) in the web page private.html
    user_snapshot: DocumentSnapshot = (
        db.collection("users").document(session["uid"]).get()
    )
    user: User = User.from_dict(user_snapshot.to_dict() | {"uid": user_snapshot.id})

    return render_template(
        "user/userinfo.html",
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        pp_filename=os.path.join("uploads", user.pp_filename),
    )


# user blueprint: Create the route /user/modify
# This route should return the template located at /user/usermodify.html when comming from GET request
# If POST, we take the form and update the data in firestore database; finally redirect to /user/info
@user_bp.route("/modify", methods=["GET", "POST"])
@authenticated
def usermodify():
    user_snapshot: DocumentSnapshot = (
        db.collection("users").document(session["uid"]).get()
    )
    user: User = User.from_dict(user_snapshot.to_dict() | {"uid": user_snapshot.id})

    if request.method == "POST":
        form_dict: dict[str, str] = {
            "firstname": request.form.get("tbx_firstname", "").strip(),
            "lastname": request.form.get("tbx_lastname", "").strip(),
            "email": request.form.get("tbx_email", "").strip(),
        }

        update_data: dict[str, str] = {}
        # Validate formular
        # remove from the update dictionnary the empty values
        for k, v in form_dict.items():
            if v != "" and v != user.to_dict()[k]:
                update_data[k] = v

        if "email" in form_dict:
            if form_dict["email"] != user.email:
                users_with_email: list[DocumentSnapshot] = (
                    db.collection("users")
                    .where("email", "==", form_dict["email"])
                    .get()
                )
                if len(users_with_email) > 0:
                    flash("Email already in use", "danger")
                    return redirect(url_for("user.usermodify"))

        if len(update_data) > 0:
            db.collection("users").document(session["uid"]).update(form_dict)

        return redirect(url_for("user.userinfo"))

    # Display user info (firstname, lastname, email) in the web page private.html

    return render_template(
        "user/usermodify.html",
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        pp_filename=os.path.join("uploads", user.pp_filename),
    )
