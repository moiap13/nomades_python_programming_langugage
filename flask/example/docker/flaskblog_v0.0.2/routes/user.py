import os, sys
ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from flask import Blueprint, session, render_template, request, flash, redirect, url_for

from config.firestore_connection import db
from helpers.decorators import authenticated
from repositories.user_firestore import (
  get_user_by_firestore_id,
  get_user_by_uid,
  get_user_by_email,
  update_user
)
from models.user import User
from exceptions.user import UserNotFoundError

user_bp = Blueprint('user', __name__, url_prefix="/user")

@user_bp.route("/info")
@authenticated
def user_info():
    user: User = get_user_by_firestore_id(session["firestore_id"], db)
    return render_template("user/userinfo.html", user=user)

@user_bp.route("/modify", methods=["GET", "POST"])
@authenticated
def user_modify():
  current_user: User = get_user_by_firestore_id(session["firestore_id"], db)

  if request.method == "POST":
    user_data: User = User.from_dict(
      {k:v for k, v in request.form.items() if v != ""} 
      | {"firestore_id": current_user.firestore_id}
    )

    if user_data.uid and user_data.uid != current_user.uid:
      try:
        get_user_by_uid(user_data.uid, db)
      except UserNotFoundError:
        pass
      else:
        flash(f"uid: {user_data.uid} already exists", "danger")
        return render_template("/user/usermodify.html", user=request.form)

    if user_data.email and user_data.email != current_user.email:
      try:
        get_user_by_email(user_data.email, db)
      except UserNotFoundError:
        pass
      else:
        flash(f"email: {user_data.email} already exists", "danger")
        return render_template("/user/usermodify.html", user=request.form)

    update_user(user_data, db)
    flash("User successfully updated", "success")
    return redirect(url_for('user.user_info'))

  return render_template("/user/usermodify.html", user=current_user)
