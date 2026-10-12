from functools import wraps

from flask import session, flash, redirect, url_for, request


def authenticated(func):
    """
    Decorator to check if user is logged in
    """

    @wraps(func)
    def inner(*args, **kwargs):
        if not session.get("loggedin", False):
            session["wanted_route"] = request.path
            flash("Please log in first", "warning")
            return redirect(url_for("login.login"))

        return func(*args, **kwargs)

    return inner
