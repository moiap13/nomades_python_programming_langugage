import os, sys
ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from flask import Blueprint, flash, redirect, url_for, render_template, session

from config.firestore_connection import db
from helpers.decorators import authenticated
from helpers.firestore_funcs import USERS_COLLECTION

from models.user import User

UPLOAD_DIR: str = os.path.join(ROOT_DIR, 'static', 'uploads')
PP_DIR: str = os.path.join(UPLOAD_DIR, 'pp')

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route("/info")
@authenticated
def user_info() -> str:
    user_firestore = db.collection(USERS_COLLECTION).document(session["firestore_id"]).get()
    if not user_firestore.exists: # Should never occur
        flash("User not found in db", "danger")
        return redirect(url_for('login.login'))
    
    user: User = User.from_dict(user_firestore.to_dict())

    if user.pp_exits(PP_DIR):
      user.pp_filename = url_for('static', filename=f'uploads/pp/{user.pp_filename}')
    else:
      user.pp_filename = user.get_pp_ui_avatars_src()
  
    return render_template("user/userinfo.html", user=user) # pass the user

# create route /modify
@user_bp.route("/modify")
def user_modify() -> str:
# TODO: this route accept both get and post requests
# TODO: Create UpdateForm using wtforms
# TODO: GET -> render_template user/usermodify.html
# TODO: POST: 
#           1. Validate the update form, based on the validators of the RegisterForm class; 
#           2. get all the values from the form and update the database document for the logged user 
#           3. redirect to /user/info route
   return "TODO"
