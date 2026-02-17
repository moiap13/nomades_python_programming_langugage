import os

from flask import Flask, render_template, request

app = Flask(__name__)

CURR_DIR: str = os.path.dirname(__file__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/name", methods=["GET", "POST"])
def name():
    if request.method == "POST":
        print(request.form)
        firstname: str = request.form.get("prenom", "Prénom par défault")
        lastname: str = request.form["nom"]
        pass
        return f"{firstname} {lastname}"
    else:
        return render_template("name/name.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
