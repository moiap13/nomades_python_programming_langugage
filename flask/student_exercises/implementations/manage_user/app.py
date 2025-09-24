import os
import json

from flask import (
    Flask,
    render_template,
    session,
    redirect,
    url_for,
    flash,
)

from routes.login import login_bp

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


@app.route("/")
def index():
    return render_template("index.html")


# TODO: Create the user blueprint file, where the name of the blueprint is user and the url prefix is /user
# this file will contain two routes the route for /user/info and the route for /user/modify
# DO not forget to register the blueprint in the app instance
# TODO: move this route to the user blueprint
@app.route("/user/info")
def userinfo() -> str:
    # if not ("loggedin" in session and session["loggedin"]):
    if not (session.get("loggedin", False)):
        flash("Please login first", "warning")
        return redirect(url_for("login"))

    # Display user info (firstname, lastname, email) in the web page private.html
    user_snapshot: DocumentSnapshot = (
        db.collection("users").document(session["uid"]).get()
    )
    user: User = User.from_dict(user_snapshot.to_dict() | {"uid": user_snapshot.id})

    return render_template(
        "user/userinfo.html",
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        pp_filename=os.path.join("uploads", user.pp_filename),
    )


# TODO: user blueprint: Create the route /user/modify
# This route should return the template located at /user/usermodify.html when comming from GET request
# If POST, we take the form and update the data in firestore database; finally redirect to /user/info

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
