import os
import json

from flask import Flask, render_template


from blueprints.login import login_bp
from blueprints.user import user_bp
from blueprints.article import article_bp


CURR_DIR: str = os.path.dirname(__file__)
CONFIG_FILE: str = os.path.join(CURR_DIR, "config", "creds.json")

with open(CONFIG_FILE) as config_file:
    config: dict[str, str] = json.load(config_file)

app = Flask(__name__)
app.secret_key = config["secret_key"]

app.register_blueprint(login_bp)
app.register_blueprint(user_bp)
app.register_blueprint(article_bp)


@app.route("/")
def index():

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
