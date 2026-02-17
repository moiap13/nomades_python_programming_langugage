from flask import Flask, render_template
import pandas as pd

app = Flask(__name__, template_folder="src")


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/var")
def var() -> str:
    return render_template("var.html", fullname="Antonio Pisanello")


@app.route("/var/<firstname>/<lastname>")
def var_dyn(firstname: str, lastname: str) -> str:
    fullname: str = f"{firstname} {lastname}"
    return render_template("var.html", fullname=fullname)


@app.route("/for")
def jinja_for():
    fruits: list[str] = [
        "apple",
        "banana",
        "orange",
        "watermelon",
        "peach",
        "strawberry",
        "kiwi",
        "pineapple",
        "mango",
        "lemon",
        "grapefruit",
    ]
    data = {"fruits": fruits}

    return render_template("for.html", data=data)


@app.route("/if")
def jinja_if():
    age = 20
    return render_template("if.html", age=age)


@app.route("/safe")
def jinja_safe():
    comment: str = "<script>alert('you ve been hacked !!')</script>"
    return render_template("safe.html", comment=comment)


@app.route("/df")
def df() -> str:
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    df_html = df.to_html()
    return render_template("df.html", df_html=df_html)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
