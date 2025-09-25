import os
import json

from flask import Flask, render_template

from routes.login import login_bp
from routes.user import user_bp

from schema.user import User
from configs.firestore_connector import db, DocumentSnapshot

CURR_DIR: str = os.path.dirname(__file__)
CONFIG_FILE: str = os.path.join(CURR_DIR, "configs", "config_creds.json")
FIRESTORE_CREDS = os.path.join(CURR_DIR, "configs", "firestore-creds.json")

with open(CONFIG_FILE) as json_config:
    config: dict[str, str] = json.load(json_config)

app = Flask(__name__)
app.config["SECRET_KEY"] = config["secret_key"]

app.register_blueprint(login_bp)
app.register_blueprint(user_bp)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
