from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index() -> str:
  return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login() -> str:
  if request.method == "POST":
    uid: str = request.form["tbx_uid"]
    pwd: str = request.form.get("tbx_pwd")

    # validate input
    if uid == "" or pwd == "":
      return "Please enter uid and pwd, please try again"
    
    print(request.form)

    # TODO: check in database if user exists with given pwd
    return f"{uid} {pwd}"
  else:
    return render_template('login.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)