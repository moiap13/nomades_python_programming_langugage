from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    print(request.form)
    email: str = request.form.get("tbx_email")
    pwd: str = request.form.get("tbx_pwd")

    if email == "antonio@test.com" and pwd == "1234567890":
      return "Login Successful"
    else:
      return "Login Unsuccessful"
  else:
    return render_template("login/login.html")

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8081, debug=True)