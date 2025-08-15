import hashlib
import os
import random
import string
import json

from flask import Flask, render_template, request, session, redirect, flash

from config.firestore_connection import db

CURR_DIR: str = os.path.dirname(__file__)
JSON_CONFIG_FILE: str = os.path.join(CURR_DIR, "config", "config.json")

with open(JSON_CONFIG_FILE) as json_config:
    config: dict[str, str] = json.load(json_config)

app = Flask(__name__)
app.config["SECRET_KEY"] = config["SECRET_KEY"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstname: str = request.form["tbx_firstname"]
        lastname: str = request.form["tbx_lastname"]
        email: str = request.form["tbx_email"]
        password: str = request.form["tbx_password"]
        password_confirmation: str = request.form["tbx_password_confirmation"]

        if (
            (
                not (
                    firstname
                    and lastname
                    and email
                    and password
                    and password_confirmation
                )
            )
            or ("@" not in email)
            or (password != password_confirmation)
        ):
            return "Please review the form"

        user = db.collection("users").where("email", "==", email).get()
        if len(user) > 0:
            flash("Email alreeady in use", "danger")
            return redirect("/register")

        salt: str = "".join(random.choices(string.ascii_uppercase, k=10))
        h_pwd: str = hashlib.sha256((password + salt).encode()).hexdigest()
        user: dict[str, str] = {
            "lastname": lastname,
            "email": email,
            "firstname": firstname,
            "password": h_pwd,
            "salt": salt,
        }
        _, doc = db.collection("users").add(user)
        print(f"User successfully registered with id {doc.id}")

        session["uid"] = doc.id
        session["firstname"] = firstname
        session["lastname"] = lastname
        session["email"] = email
        session["loggedin"] = True
        flash("User successfully registered", "success")
        return redirect("/home")
    else:
        return render_template("login/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email: str = request.form.get("tbx_email", "")
        password: str = request.form.get("tbx_password", "")

        if not (email and password) or "@" not in email:
            flash("Please review the login form", "danger")
            return redirect("/login")

        user = db.collection("users").where("email", "==", email).get()
        if len(user) == 0:
            flash("User not in database", "danger")
            return redirect("/login")

        user_data = user[0].to_dict()

        salt = user_data.get("salt", "99999999")
        h_pwd = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()

        if h_pwd != user_data["password"]:
            flash("Wrong credentials", "danger")
            return redirect("/login")

        session["uid"] = user[0].id
        session["firstname"] = user_data.get("firstname")
        session["lastname"] = user_data.get("lastname")
        session["email"] = user_data.get("email")
        session["loggedin"] = True
        flash("Logged in successfully", "success")
        return redirect("/home")
    else:
        return render_template("login/login.html")


@app.route("/logout")
def logout():
    session["loggedin"] = False
    session.pop("loggedin")
    session.clear()
    flash("Successfully logged out", "success")
    return redirect("/login")


# Add a new route for private part
# This route should be available only when someone is logged in
# Otw -> show message to login
@app.route("/private")
def private():
    if "loggedin" in session and session["loggedin"]:
        return "Private part !"
    else:
        return redirect("/login")


@app.route("/home")
def home():
    if not ("loggedin" in session and session["loggedin"]):
        flash("Login first", "warning")
        return redirect("/login")

    return render_template(
        "user/home.html",
        firstname=session["firstname"],
        lastname=session["lastname"],
        email=session["email"],
    )


@app.route("/posts/add", methods=["GET", "POST"])
def add_post():
    if not ("loggedin" in session and session["loggedin"]):
        flash("Login first", "warning")
        return redirect("/login")

    if request.method == "POST":
        title: str = request.form["tbx_title"]
        body: str = request.form["tbx_body"]

        if not (title and body):
            flash("Please review the form", "danger")
            return redirect("/posts/add")

        post: dict[str, str] = {
            "title": title,
            "body": body,
            "author": db.collection("users").document(session["uid"]),
        }
        db.collection("posts").add(post)

        return redirect("/posts/list/my")

    return render_template("post/add.html")


@app.route("/posts/list")
def list_posts():
    if not ("loggedin" in session and session["loggedin"]):
        flash("Login first", "warning")
        return redirect("/login")

    user_ref = db.document(f"users/{session['uid']}")
    posts: list[dict[str, str]] = [
        post.to_dict() | {"id": post.id, "mine": post.to_dict()["author"] == user_ref}
        for post in db.collection("posts").get()
    ]
    return render_template("post/list.html", posts=posts)


@app.route("/posts/list/my")
def list_my_posts():
    if not ("loggedin" in session and session["loggedin"]):
        flash("Login first", "warning")
        return redirect("/login")

    posts: list[dict[str, str]] = [
        post.to_dict() | {"id": post.id}
        for post in db.collection("posts")
        .where("author", "==", db.document(f"users/{session['uid']}"))
        .get()
    ]
    return render_template("post/list.html", posts=posts)


@app.route("/posts/delete/<post_id>")
def delete_post(post_id: str):
    if not ("loggedin" in session and session["loggedin"]):
        flash("Login first", "warning")
        return redirect("/login")

    post_ref = db.collection("posts").document(post_id)
    post_data = post_ref.get().to_dict()
    if post_data["author"] == db.collection("users").document(session["uid"]):
        flash("Post successfully deleted", "success")
        post_ref.delete()
    else:
        flash("You are not the author of the post", "danger")

    return redirect("/posts/list/my")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
