from functools import wraps

from flask import session, redirect, url_for, flash


def authenticated(func):
  @wraps(func)
  def inner_function(*args, **kwargs):
    # protect this route
    if not ("loggedin" in session and session["loggedin"] == True):
        # I'm not logged in !!
        flash("Please login first", "warning")
        return redirect(url_for('login'))

    return func(*args, **kwargs)
  return inner_function

