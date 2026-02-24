import os
import sys

ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from flask import Blueprint, render_template, session, url_for

from helpers.decorators import authenticated
from helpers.filesystem import verify_upload_exists

from database.user_repository import UserRepository

from models.user import User

user_bp = Blueprint("user", __name__, url_prefix="/user")
_user_repository = UserRepository("users")


@user_bp.route("/info")
@authenticated
def userinfo():
    user: User = _user_repository.get_user_by_firestore_id(session["firestore_id"])
    assert user is not None

    pp_path: str = (
        url_for("static", filename="uploads/" + user.avatar)
        if verify_upload_exists(user.avatar)
        else user.get_ui_avatar_url()
    )
    return render_template("user/userinfo.html", user=user.to_dict(), pp_path=pp_path)


@user_bp.route("/api/info")
def api_userinfo():
    user: User = _user_repository.get_user_by_firestore_id(session["firestore_id"])
    assert user is not None
    return user.to_dict(), 200
