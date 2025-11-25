from flask import Flask, url_for, render_template

app: Flask = Flask(__name__)


@app.route("/")
def index() -> str:
    return f"""<h1>Hello World !<h1>
    <br/>
    <p>Welcome to this python week about flask programming</p>"""


@app.route("/antonio")
def antonio() -> str:
    n = "My name is Antonio"


@app.route("/hello/<name>")
def hello(name: str):
    return f'<h1>Hello <span style="color: red;">{name.capitalize()}</span></h1>'


@app.route("/age/<int:age>")
def show_age(age: int):
    return f"The giver age is {age}"


@app.route("/hello/<name>/<int:age>")
def hello_name_age(name: str, age: int):
    return f"<h1>Hello I'm <span style=\"color: red;\">{name.capitalize()}</span> and I'm {age} years old !</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
