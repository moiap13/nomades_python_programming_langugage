import os
import json

from flask import Flask, session, request, render_template, redirect, url_for

CURR_DIR: str = os.path.dirname(__file__)
CONFIG_FILE: str = os.path.join(CURR_DIR, "configs", "config_creds.json")

with open(CONFIG_FILE) as json_config:
    config: dict[str, str] = json.load(json_config)

app = Flask(__name__)
app.config["SECRET_KEY"] = config["secret_key"]


@app.route("/count/add")
def count() -> str:
    counter: int = session.get("counter", 0)
    counter += 1
    session["counter"] = counter
    return f"Counter: {counter}"


@app.route("/count/show")
def show_count() -> str:
    if "counter" in session:
        return f"Counter: {session['counter']}"
    return "No session right now please go to /count/add to create a session"


@app.route("/signin", methods=["GET", "POST"])
def login() -> str:
    if request.method == "POST":
        # 1. Get the data from form
        email: str = request.form.get("tbx_email", "")
        pwd: str = request.form.get("tbx_password", "")

        # 2. Validate the datas
        if email == "" or pwd == "":
            return "Please fill the form correctly !"

        # 3. Check login
        if email == "admin@admin.ch" and pwd == "admin":
            # If loggin worked
            session["loggedin"] = True
            return redirect(url_for("private"))

        # If login failed
        return "Login failed !"
    else:
        # GET call
        return render_template("login/login.html")


@app.route("/private")
def private() -> str:
    if not session.get("loggedin", False):
        return redirect(url_for("login"))

    return "Welcome to the private part"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
