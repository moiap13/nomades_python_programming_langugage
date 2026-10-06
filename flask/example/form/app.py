from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index() -> str:
  return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login() -> str:
  if request.method == "POST":
    print(request.form)
    uid: str = request.form["uid"]
    pwd: str = request.form.get("pwd", "")

    # Validation
    if uid == "" or pwd == "":
      return "Please fill out the form"

    # TODO: login logic
    return f"{uid} - {pwd}"
  else:
    return render_template('login.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000, debug=True)