import os
import json
from hashlib import sha256

from flask import Flask, render_template, request, session, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials, firestore

from helpers.firestore_funcs import get_user_by_uid, USERS_COLLECTION
from helpers.password_generator import generate_password as generate_salt
from helpers.decorators import authenticated
from forms.login import RegisterForm


CURR_DIR: str = os.path.dirname(__file__)
FIRESTORE_CREDS: str = os.path.join(CURR_DIR, 'config', 'firestore-creds.json')

with open(os.path.join(CURR_DIR, "config", "creds.json")) as json_config:
    config: dict[str, str] = json.load(json_config)

app = Flask(__name__)
app.config["SECRET_KEY"] = config["secret_key"]

# Connection a firebase
cred = credentials.Certificate(FIRESTORE_CREDS)
firebase_admin.initialize_app(cred)# Connection a firestore
db = firestore.client()
print(db)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register function should add a new user to the users.csv file
    """
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        # 1. Get the data
        # get the user uid from form
        uid: str = form.uid.data
        # get the user password from form
        pwd: str = form.pwd.data
        firstname: str = form.firstname.data
        lastname: str = form.lastname.data
        email: str = form.email.data
        age: int = form.age.data

        # 3. Logic
        # (BONUS): Check if user already exists in csv file, if so -> return "User already exists"
        if get_user_by_uid(uid, db) != None:
            return "Error: User already exists"
        
        salt: str = generate_salt(True, False, False, False, 10)
        h_pwd: str = sha256((pwd+salt).encode()).hexdigest()

        _, doc = db.collection(USERS_COLLECTION).add({
            "uid": uid,
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "age": age,
            "pwd": h_pwd,
            "salt": salt
        })

        session["loggedin"] = True
        session["uid"] = uid
        session["firestore_id"] = doc.id

        flash(f"User {uid} successfully registered", "success")

        return redirect(url_for("user_info"))
    else:
        # GET
        return render_template("login_wtf/register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    The login functiojn should authenticate a user using his uid and pwd
    """
    if request.method == "POST":
        # 1. Get the datas
        uid: str = request.form["uid"]
        pwd: str = request.form["pwd"]

        # 2. Validate
        if uid == "" or pwd == "":
            return "Error: please fill the form"

        # 3. Logic
        # Open in "r" mode the users csv file using the constant CSV_FILE
        user: dict[str, str] | None = get_user_by_uid(uid, db)
        if user:
            salt: str = user.get("salt", "")
            h_pwd: str = sha256((pwd + salt).encode()).hexdigest()
            if user["pwd"] == h_pwd:
                # if login successful -> return "Login successful"
                flash("Login successful", "success")
                session["loggedin"] = True
                session["uid"] = uid
                session["firestore_id"] = user["id"]

                return redirect(url_for("user_info"))

        # otw, return "Wrong credentials"
        return "Wrong Credentials"
    else:
        return render_template("login/login.html")

@app.route("/logout")
def logout():
    # logout the user; think about session
    session["loggedin"] = False
    session.pop("loggedin")
    session.clear() 
    # redirect to login route
    flash("logout successful", "success")
    return redirect(url_for('login'))

@app.route("/user/info")
@authenticated
def user_info() -> str:
    # assert(session["loggedin"] == True)
    # get the user informations (CSV or session as you want)
    
    user = db.collection(USERS_COLLECTION).document(session["firestore_id"]).get()
    if not user.exists: # Should never occur
        return redirect(url_for('login'))
    user_data: dict[str, str | int] = user.to_dict()

    return render_template("user/userinfo.html", user=user_data) # pass the user

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
