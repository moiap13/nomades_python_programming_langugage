import os

from flask import Flask, render_template, request

app = Flask(__name__)

CURR_DIR: str = os.path.dirname(__file__)
UPLOAD_DIR: str = os.path.join(CURR_DIR, "uploads")

@app.route("/")
def index() -> str:
  return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login() -> str:
  if request.method == "POST":
    # 1. recupere les donnes
    uid: str = request.form["tbx_uid"]
    pwd: str = request.form.get("tbx_pwd", "")

    # 2. Valide les donnees
    if uid == "" or pwd == "":
      return "Error: please fill out the form"
    
    # if "@" not in uid:
    #   return "Error: Please èrovide an email adress"

    # 3. Buisness logic

    # TODO: check if user in database
    return f"User data: uid={uid}, pwd={pwd}"
  else:
    return render_template("login/login.html")
  

# @app.route("/login", methods=["GET"])
# def login() -> str:
  
#   return render_template("login/login.html")
  
# @app.route("/login_post", methods=["POST"])
# def login_post() -> str:
#   uid: str = request.form["tbx_uid"]
#   pwd: str = request.form.get("tbx_pwd", "")

#   # TODO: check if user in database
#   return f"User data: uid={uid}, pwd={pwd}"

@app.route("/files", methods=["GET", "POST"])
def send_files() -> str:
  if request.method == "POST":
    accepted_format: list[str] = ["image/png", "image/jpeg"]
    imgs = request.files.getlist("fileInput")
    img_name = request.form.get("img_name")
    for i, img in enumerate(imgs):
      if img.content_type in accepted_format:
        # img.save(os.path.join(UPLOAD_DIR, img.filename))
        img.save(os.path.join(UPLOAD_DIR, f"{img_name}_{i}"))
    return ""
  else:
    return render_template("input_file.html")

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True)
