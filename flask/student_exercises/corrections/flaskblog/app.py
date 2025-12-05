import os
import json

from flask import Flask, render_template, flash

from config.firestore_connection import db

from routes.login import login_bp
from routes.user import user_bp
from routes.search import search_bp
from routes.articles import articles_bp
from routes.statistics import statistics_bp
from routes.map import map_bp

CURR_DIR: str = os.path.dirname(__file__)
CONFIG: str = os.path.join(CURR_DIR, "config", "creds.json")
UPLOAD_DIR: str = os.path.join(CURR_DIR, "static", "uploads")
USERS_JSON: str = os.path.join(CURR_DIR, "data", "users.json")

with open(CONFIG) as json_config:
    config: dict[str, str] = json.load(json_config)

app = Flask(__name__)
app.config["SECRET_KEY"] = config["secret_key"]
app.register_blueprint(login_bp)
app.register_blueprint(user_bp)
app.register_blueprint(search_bp)
app.register_blueprint(articles_bp)
app.register_blueprint(statistics_bp)
app.register_blueprint(map_bp)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/populate_db")
def populate_db():
    with open(USERS_JSON) as json_users:
        users: list[dict[str, int | str | dict[str, str]]] = json.load(json_users)
        for user in users:
            db.collection("users").document(user["email"]).set(user)
    flash("Database populated", "success")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
