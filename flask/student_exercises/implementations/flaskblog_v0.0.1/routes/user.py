import os, sys

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
sys.path.append(ROOT_DIR)

from uuid import uuid4

from flask import Blueprint, Response, session, render_template, request, redirect, url_for, flash

from helpers.decorators import authenticated
from repositories.users_repository_firestore import (
  get_user_by_firestore_id, 
  get_user_by_uid, 
  get_user_by_email,
  update_user,
  delete_user_pp
)
from config.firestore_config import db
from exceptions.user import UserNotFoundError
from forms.user import UserModifyForm
from models.user import User

UPLOAD_FOLDER: str = os.path.join(ROOT_DIR, 'static', 'uploads')

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route("/info")
@authenticated
def user_info() -> str:
  # user: dict[str, str] = get_user_by_uid(db, session["uid"])
  try:
      user: User = get_user_by_firestore_id(db, session["firestore_id"])
  except ValueError:
      user: User = get_user_by_firestore_id(db, str(session["firestore_id"]))
  except UserNotFoundError:
      return redirect(url_for("login.logout"))
  
  return render_template('user/userinfo.html', user=user)

@user_bp.route("/modify", methods=["GET", "POST"])
@authenticated
def user_modify() -> str:
    user: User = get_user_by_firestore_id(db, session["firestore_id"])
    form = UserModifyForm(request.form, data=request.files)

    if request.method == "POST" and form.validate():
        updated_user = User(
          uid=form.uid.data,
          firstname=form.firstname.data,
          lastname=form.lastname.data,
          email=form.email.data
        )

        pp: "FileStorage" = form.pp.data

        if updated_user.email != user.email:
          try:
            get_user_by_email(db, updated_user.email)
          except UserNotFoundError: 
            pass
          else:
            flash(f"User with email={updated_user} already exists", "danger")
            return render_template("user/usermodify.html", user=request.form)

        if updated_user.uid != user.uid:
          try:
            get_user_by_uid(db, updated_user.uid)
            flash(f"User with uid={updated_user.uid} already exists", "danger")
            return render_template("user/usermodify.html", user=request.form)
          except UserNotFoundError: 
            pass

        if pp:
          if user.pp_filename:
            pp_path = os.path.join(UPLOAD_FOLDER, user.pp_filename)
            if os.path.exists(pp_path):
              os.remove(pp_path)

          pp_ext = pp.filename.split('.')[-1]
          pp_filename = f'{uuid4()}.{pp_ext}'
          pp.save(os.path.join(UPLOAD_FOLDER, pp_filename))
          updated_user.pp_filename = pp_filename
        
        #  3. Update the database document for the logged user (use the update function from the firestore repo)
        # Handle file update in the update function
        update_user(db, session["firestore_id"], updated_user)

        #  4. redirect to /user/info route
        flash("User successfully updated", "success")
        return redirect(url_for("user.user_info"))

            
    # GET -> render_template user/usermodify.html
    return render_template("user/usermodify.html", user=user, form=form)

@user_bp.route("/delete/pp")
@authenticated
def user_delete_pp() -> str:
   delete_user_pp(db, session["firestore_id"])
   flash("PP successfully deleted", "success")
   return redirect(url_for("user.user_info"))