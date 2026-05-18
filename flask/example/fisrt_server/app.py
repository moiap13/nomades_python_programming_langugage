from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, FlaskWeek PPL_2026_2T"

@app.route("/index")
def index():
    return '<h1>Hello <span style="color: red;">PPL 2026 2T</span></h1><a href="https://google.com">Click here</a>'

@app.route('/allow/<int:age>')
def allow_voting(age):
    return "You are allowed to enter the voting website" if age >= 18 else "You are not allowed to enter the voting website"

@app.route('/allow/<age>')
def allow_voting_str(age):
    return age

@app.route('/allow/22a')
def r22a():
    return "Static route 22a"



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
