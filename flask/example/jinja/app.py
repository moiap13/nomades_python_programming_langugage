from flask import Flask, render_template
import pandas as pd

app: Flask = Flask(__name__, template_folder="bootstrap")


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/user/view")
def view_user() -> str:
    return "View user"


@app.route("/user/add")
def add_user() -> str:
    return "Add user"


@app.route("/hello/<name>")
def hello(name: str) -> str:
    return f'<h1>Welcome <span style="color:red;">{name.capitalize()}</span></h1>'


# @app.route("/hello/<name>/<lastname>")
# def hello2(name: str, lastname: str) -> str:
#     return f'<h1>Welcome <span style="color:red;">{name.capitalize()}</span> {lastname}</h1>'


@app.route("/hello/<float:age>")
def hello_age(age: int) -> str:
    a = "Major" if age >= 18 else "Minor"
    return f"<h1>You are {a}</h1>"


@app.route("/var/<uid>")
def var(uid: str) -> str:
    return render_template("var.html", username=uid, years=23)


@app.route("/for")
def jinja_for():
    fruits: list[str] = [
        "apple",
        "banana",
        "orange",
        "watermelon",
        "peach",
    ]

    return render_template("for.html", fruits=fruits)


@app.route("/if")
def jinja_if():
    age = 20
    return render_template("if.html", age=age)


@app.route("/filter")
def jinja_filter() -> str:
    return render_template("filter.html", username="antonio")


@app.route("/safe")
def jinja_safe() -> str:
    html: str = '<script>alert("You got Hacked !!!!")</script>'
    return render_template("safe.html", html=html)


@app.route("/pandas")
def jinja_pandas_safe():
    df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", '<script>alert("You got Hacked !!!!")</script>'],
            "age": [25, 30, 35],
        }
    ).set_index("id")
    html: str = df.to_html()
    return render_template("safe.html", html=html)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
