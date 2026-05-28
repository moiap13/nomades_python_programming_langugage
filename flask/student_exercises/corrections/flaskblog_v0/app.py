import os
import json

from flask import Flask, render_template

from routes.login import login_bp
from routes.user import user_bp
from routes.post import post_bp
from routes.post_rest import post_bp_rest

CURR_DIR: str = os.path.dirname(__file__)

with open(os.path.join(CURR_DIR, "config", "creds.json")) as json_config:
    config: dict[str, str] = json.load(json_config)

app = Flask(__name__)
app.config["SECRET_KEY"] = config["secret_key"]

app.register_blueprint(login_bp)
app.register_blueprint(user_bp)
app.register_blueprint(post_bp)
app.register_blueprint(post_bp_rest)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
