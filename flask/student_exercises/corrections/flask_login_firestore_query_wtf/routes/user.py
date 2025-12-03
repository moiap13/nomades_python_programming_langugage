import sys
import os

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
sys.path.append(ROOT_DIR)

from hashlib import sha256

from flask import Blueprint, url_for, render_template, session, redirect, request, flash

from config.firestore_connection import db, DocumentReference

from helpers.decorators import authenticated
from helpers.errors import UserNotFoundError
from helpers.firestore_funcs import get_user_by_uid, get_user_by_email
from helpers.password_generator import generate_password as generate_salt
from helpers.files import generate_pp_filename

from forms.user import UserModifyForm

UPLOAD_DIR: str = os.path.join(ROOT_DIR, "static", "uploads")

user_bp: Blueprint = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/info")
@authenticated
def user_info() -> str:
    # try:
    #     user: dict[str, str] = get_user_by_uid(session["uid"], db)
    # except UserNotFoundError:
    #     flash("User not found", "danger")
    #     return redirect("logout")
    user: dict[str, str | int] = (
        db.collection("users").document(session["firestore_id"]).get().to_dict()
    )
    img_path = url_for(
        "static", filename=os.path.join("uploads", user.get("pp_filename", "UNKNOWN"))
    )
    user["pp_filename"] = (
        img_path
        if os.path.isfile(os.path.join(UPLOAD_DIR, user.get("pp_filename", "UNKNOWN")))
        else f"https://ui-avatars.com/api/?name={user["firstname"]}+{user["lastname"]}&background=random"
    )

    return render_template("user_wtf/userinfo.html", user=user)


@user_bp.route("/modify", methods=["GET", "POST"])
def user_modify():
    # Allow the user to modify bith email and uid
    # email and uid must be unique in database
    form = UserModifyForm(request.form, data=request.files)
    try:
        user: dict[str, str | int] = get_user_by_uid(session["uid"], db)
    except UserNotFoundError:
        flash("Error: user not found", "danger")
        return redirect(url_for("user.user_info"))

    if request.method == "POST" and form.validate():
        firstname: str = form.firstname.data
        lastname: str = form.lastname.data
        uid: str = form.uid.data
        email: str = form.email.data
        old_pwd: str = form.old_pwd.data
        new_pwd: str = form.new_pwd.data
        age: int = form.age.data
        pp = form.pp.data

        if (old_pwd != "" and new_pwd == "") or (old_pwd == "" and new_pwd != ""):
            flash("Please enter both old and new password fields", "danger")
            return render_template("user_wtf/usermodify.html", form=form)

        if uid != user["uid"]:
            try:
                get_user_by_uid(uid, db)
            except UserNotFoundError:
                session["uid"] = uid
            else:
                flash(f"User id = {uid} already exists in database", "danger")
                return render_template("user_wtf/usermodify.html", form=form)
        if email != user["email"]:
            try:
                get_user_by_email(email, db)
            except UserNotFoundError:
                pass
            else:
                flash(f"Email = {email} already exists in database", "danger")
                return render_template("user_wtf/usermodify.html", form=form)

        new_salt: str = ""
        h_new_pwd: str = ""
        if old_pwd != "" and new_pwd != "":
            h_old_pwd: str = sha256(
                (old_pwd + user.get("salt", "")).encode()
            ).hexdigest()
            if h_old_pwd != user["pwd"]:
                flash("Old password error", "danger")
                return render_template("user_wtf/usermodify.html", form=form)

            new_salt = generate_salt(True, False, False, False, 10)
            h_new_pwd = sha256((new_pwd + new_salt).encode()).hexdigest()

        user_doc_ref: DocumentReference = db.collection("users").document(
            session["firestore_id"]
        )

        if pp:
            pp_filename: str = generate_pp_filename(pp.filename)
            pp.save(os.path.join(UPLOAD_DIR, pp_filename))

        user_doc_ref.update(
            {
                "firstname": firstname,
                "lastname": lastname,
                "uid": uid,
                "email": email,
                "age": age,
                "pwd": h_new_pwd if h_new_pwd != "" else user["pwd"],
                "salt": new_salt if new_salt else user["salt"],
                "pp_filename": (
                    pp_filename
                    if pp
                    else (user["pp_filename"] if user.get("pp_filename") else "")
                ),
            }
        )

        flash("User updated successfully", "success")
        return redirect(url_for("user.user_modify"))
    else:
        form.uid.data = user["uid"]
        form.firstname.data = user["firstname"]
        form.lastname.data = user["lastname"]
        form.email.data = user["email"]
        form.age.data = user["age"]
        return render_template("user_wtf/usermodify.html", form=form)
