# TODO: Create a Blueprint for handling search route
# TODO: The search route accepts GET and POST methods
# TODO: Get -> returns the search page
# TODO: POST -> Do the search on uid, email, firstname, lastname /!\ firestore don't do substring search
# TODO: /!\ a person can be found multiple times
import sys
import os

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
sys.path.append(ROOT_DIR)

from flask import Blueprint, request, render_template

from config.firestore_connection import db

from helpers.errors import UserNotFoundError
from helpers.firestore_funcs import (
    get_user_by_uid,
    get_user_by_email,
    get_users_by_firstname,
    get_users_by_lastname,
)

search_bp: Blueprint = Blueprint("search", __name__)


@search_bp.route("/search", methods=["GET", "POST"])
def search() -> str:
    if request.method == "POST":
        search_term: str = request.form.get("tbx_search", "")

        try:
            uid_user: dict = get_user_by_uid(search_term, db)
        except UserNotFoundError:
            uid_user = None

        try:
            email_user: dict = get_user_by_email(search_term, db)
        except UserNotFoundError:
            email_user = None

        firstname_users: list[dict] = get_users_by_firstname(search_term, db)
        lastname_users: list[dict] = get_users_by_lastname(search_term, db)

        result_users: list[dict] = (
            [uid_user, email_user] + firstname_users + lastname_users
        )

        return render_template(
            "search/search.html", users=[user for user in result_users if user != None]
        )
