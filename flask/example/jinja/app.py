from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/var")
def var() -> str:
    firstname: str = "aNtOnIo"
    lastname: str = "Pisanello"
    full_name: str = f"{firstname} {lastname}"
    return render_template("var.html", name=full_name)


@app.route("/for")
def for_() -> str:
    fruits: list[str] = [
        "apple",
        "banana",
        "watermelon",
        "peach",
        "strawberry",
        "orange",
        "kiwi",
        "lemon",
        "grape",
        "melon",
    ]
    return render_template("for.html", fruits=fruits)


@app.route("/if")
def if_() -> str:
    age: int = 17
    return render_template("if.html", age=age)


@app.route("/safe")
def safe() -> str:
    safe_html = "<script>alert('You got Hacked !!')</script>"
    return render_template("safe.html", safe_html=safe_html)


@app.route("/df")
def df() -> str:
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    df_html = df.to_html()
    return render_template("df.html", df_html=df_html)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
