import os, sys
ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from flask import Blueprint, flash, redirect, request, url_for, render_template, session

from config.firestore_connection import db
from helpers.decorators import authenticated
from helpers.firestore_funcs import USERS_COLLECTION
from forms.user import UserModifyForm
from repositories.user import UserRepository
from models.user import User
from exceptions.user import UserNotFoundError

UPLOAD_DIR: str = os.path.join(ROOT_DIR, 'static', 'uploads')
PP_DIR: str = os.path.join(UPLOAD_DIR, 'pp')

user_bp = Blueprint('user', __name__, url_prefix='/user')
user_repository = UserRepository()

@user_bp.route("/info")
@authenticated
def user_info() -> str:
    try:
      user: User = user_repository.get_by_firestore_id(session['firestore_id']) 
    except UserNotFoundError as e: # should never happen
       flash(str(e), "danger")
       return redirect(url_for('login.login'))

    if user.pp_exits(PP_DIR):
      user.pp_filename = url_for('static', filename=f'uploads/pp/{user.pp_filename}')
    else:
      user.pp_filename = user.get_pp_ui_avatars_src()
  
    return render_template("user/userinfo.html", user=user) # pass the user

# create route /modify
# this route accept both get and post requests
@user_bp.route("/modify", methods=["GET", "POST"])
@authenticated
def user_modify() -> str:
    # Create UpdateForm using wtforms
    form = UserModifyForm(request.form)

    try:
      user: User = user_repository.get_by_firestore_id(session['firestore_id']) 
    except UserNotFoundError as e: # should never happen
       flash(str(e), "danger")
       return redirect(url_for('login.login'))

    if user.pp_exits(PP_DIR):
      user.pp_filename = url_for('static', filename=f'uploads/pp/{user.pp_filename}')
    else:
      user.pp_filename = user.get_pp_ui_avatars_src()

    if request.method == "POST" and form.validate():
      # POST: 
      #   1. Validate the update form, based on the validators of the RegisterForm class; 
      #   2. get all the values from the form and update the database document for the logged user 
      #   3. redirect to /user/info route
      user.firstname = form.firstname.data
      user.lastname = form.lastname.data
      user.uid = form.uid.data
      user.email = form.email.data
      user.age = form.age.data

      user_repository.update(user, ['id', 'salt', 'pwd', 'pp_filename'])

      return redirect(url_for('user.user_info'))
    
    # GET -> render_template user/usermodify.html
    return render_template('user/usermodify.html', form=form, user=user)
