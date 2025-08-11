import random
from flask import Flask

app: Flask = Flask(__name__)


@app.route("/")
def index() -> str:
    return '<h1 style="color: purple;">Hello Nomades <span style="color: red;">PPL_2025_0708</span></h1><ol><li>Nathalie</li><li>Pietro</li><li>...</li><li>Martin</li></ol>'


@app.route("/random_")
def random_():
    return str(random.randint(1, 12))


@app.route("/random__")
def random__():
    return str(random.randint(100, 1200))


@app.route("/hello/<name>")
def hello_name(name: str) -> str:
    return (
        f'<h1 style="color: purple;">Hello <span style="color: red;">{name}</span></h1>'
    )


@app.route("/hello/<firstname>/<lastname>")
def hello_full_name(firstname: str, lastname: str) -> str:
    return f'<h1 style="color: purple;">Hello <span style="color: red;">{firstname}</span><span style="color: yellow;">{lastname}</span></h1>'


@app.route("/age/<int:age>")
def hello_age(age: int) -> str:
    return f'<h1 style="color: purple;">Hello, you are <span style="color: red;">{age}</span> years old</h1>'


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)
