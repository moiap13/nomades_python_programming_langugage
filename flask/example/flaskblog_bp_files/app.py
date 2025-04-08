import os
import json

CURR_DIR = os.path.dirname(__file__)
CONFIG_FILE_PATH = os.path.join(CURR_DIR, "config", "server-creds.json")

from flask import Flask, render_template, session, redirect, url_for, flash

from src.login.login_bp import login_bp
from src.posts.posts_bp import post_bp
from helpers.decorators import authenticated

with open(CONFIG_FILE_PATH, "r") as json_config:
  config = json.load(json_config)
  
app = Flask(__name__)
app.config["SECRET_KEY"] = config["SECRET_KEY"]

app.register_blueprint(login_bp)
app.register_blueprint(post_bp)

@app.route("/userinfo")
@authenticated
def userinfo():
  # Get the user infos from the session and pass them to the template
  return render_template("user/user_info.html", user=session["user"])

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8081, debug=True)