import os

from flask import Flask, render_template, request

app = Flask(__name__)

CURR_DIR: str = os.path.dirname(__file__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    if request.method == "POST":
        # 1. get the datas
        email: str = request.form["tbx_email"]
        pwd: str = request.form.get("tbx_pwd", "")
        print(email, pwd)

        # 2. validate the datas
        if not (email == "" and pwd == ""):
            return "Error: please provide email and/or password"

        if "@" not in email:
            return "Error: please provide email address valid"

    return render_template("login/login.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
