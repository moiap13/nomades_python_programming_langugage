from functools import wraps

from flask import session, flash, redirect, url_for


def authenticated(f):
    @wraps(f)
    def inner_func(*args, **kwargs):
        # if not ("loggedin" in session and session["loggedin"]):
        if not (session.get("loggedin", False)):
            flash("Please login first", "warning")
            return redirect(url_for("login.login"))

        return f(*args, **kwargs)

    return inner_func
