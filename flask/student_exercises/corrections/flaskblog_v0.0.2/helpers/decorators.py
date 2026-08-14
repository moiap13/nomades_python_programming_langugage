from functools import wraps

from flask import session, flash, redirect, url_for

def authenticated(f: "function") -> "function":
  @wraps(f)
  def inner_func(*args, **kwargs):
    if not session.get("loggedin", False):
      flash("Login first", "warning")
      return redirect(url_for("login")) 

    return f(*args, **kwargs)
  return inner_func