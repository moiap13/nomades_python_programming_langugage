import os, sys

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
sys.path.append(ROOT_DIR)

from uuid import uuid4

from flask import Blueprint, Response, session, render_template, request, redirect, url_for, flash
import folium

from helpers.decorators import authenticated

from exceptions.user import UserEmailAlreadyExistsError, UserNotFoundError, UserUidAlreadyExistsError
from forms.user import UserModifyForm
from models.user import User
from services.user import UserService

UPLOAD_FOLDER: str = os.path.join(ROOT_DIR, 'static', 'uploads')

user_bp = Blueprint('user', __name__, url_prefix='/user')

user_service = UserService()

@user_bp.route("/info")
@authenticated
def user_info() -> str:
  # user: dict[str, str] = get_user_by_uid(db, session["uid"])
  try:
      user: User = user_service.get_user_by_firestore_id(session["firestore_id"])
  except ValueError:
      user: User = user_service.get_user_by_firestore_id(session["firestore_id"])
  except UserNotFoundError:
      return redirect(url_for("login.logout"))
  
  return render_template('user/userinfo.html', user=user)

@user_bp.route("/modify", methods=["GET", "POST"])
@authenticated
def user_modify() -> str:
    user: User = user_service.get_user_by_firestore_id(session["firestore_id"])
    form = UserModifyForm(request.form, data=request.files)

    if request.method == "POST" and form.validate():
        updated_user = User(
          uid=form.uid.data,
          firstname=form.firstname.data,
          lastname=form.lastname.data,
          email=form.email.data,
          firestore_id=session["firestore_id"]
        )

        pp: "FileStorage" = form.pp.data
                
        if pp:
          if user.pp_filename:
            pp_path = os.path.join(UPLOAD_FOLDER, user.pp_filename)
            if os.path.exists(pp_path):
              os.remove(pp_path)

          pp_ext = pp.filename.split('.')[-1]
          pp_filename = f'{uuid4()}.{pp_ext}'
          pp.save(os.path.join(UPLOAD_FOLDER, pp_filename))
          updated_user.pp_filename = pp_filename

        try: 
          user = user_service.modify_user(updated_user)
        except UserEmailAlreadyExistsError:
          flash(f"User with email={updated_user.email} already exists", "danger")
          return render_template("user/usermodify.html", user=request.form)
        except UserUidAlreadyExistsError:
          flash(f"User with uid={updated_user.uid} already exists", "danger")
          return render_template("user/usermodify.html", user=request.form)
    
        flash("User successfully updated", "success")
        return redirect(url_for("user.user_info"))
        
    # GET -> render_template user/usermodify.html
    return render_template("user/usermodify.html", user=user, form=form)

@user_bp.route("/delete/pp")
@authenticated
def user_delete_pp() -> str:
   user_service.delete_user_pp(session["firestore_id"])

   flash("PP successfully deleted", "success")
   return redirect(url_for("user.user_info"))

@user_bp.route("/location")
def user_location() -> str:
  users: list[User] = user_service.get_all()

  m = folium.Map(location=(46.2044, 6.1432))

  for user in users:
     folium.Marker(
          location=list(user.geo_position.values()),
          tooltip=user.uid,
          popup=render_template(
              "user/components/tooltip.html",
              user=user
          ),
      ).add_to(m)
  
  return render_template(
    "user/userlocation.html",
    map_html=m._repr_html_(),
  )