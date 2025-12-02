from functools import wraps

from flask import session, redirect, url_for, flash


def authenticated(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        if not ("loggedin" in session and session["loggedin"] == True):
            flash("Please login first !", "warning")
            return redirect(url_for("login"))

        return func(*args, **kwargs)

    return inner_func
