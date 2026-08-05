from flask import Flask

app = Flask(__name__)

@app.route("/")
def index() -> str:
  return "Hello World !"

@app.route("/hello")
def index_nomades() -> str:
  return "<h1>Hello in this nomade's course about <span style='color: orange;'>flask !</span></h1><img src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRibW8ClDdk-676yWj4Zug9WLv7OqU5b7eYsGCp5KzM-2sYzujJdwUrwu-VxcA2-QnfpOVe1Q&s=10' alt='dog' />"

@app.route("/hello/<name>")
def hello_name(name: str) -> str:
  return f"<h1>Hello <span style='color: red;'>{name}</span> !</h1>"

@app.route('/allow/<int:age>')
def allow_voting(age: int):
    return "You are allowed to enter the voting website" if age >= 18 else "You are not allowed to enter the voting website"

@app.route('/allow/<age>')
def allow_voting_str(age: str):
  return age



if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True)