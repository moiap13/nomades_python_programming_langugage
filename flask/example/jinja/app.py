from datetime import datetime

from flask import Flask, render_template
import pandas as pd

app = Flask(__name__, template_folder="src")

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/variable/<name>")
def var(name: str):
  time: str = datetime.now().strftime("%H:%M:%S")
  return render_template("var.html", time_str=time, name=name)

@app.route("/for")
def for_():
  fruits: list[str] = [
    "Banana",
    "Strawberry",
    "Peach",
    "Apple",
    "Watermelon",
    "Orange",
    "Kiwi",
    "Pineapple",
    "Mango"
  ]
  return render_template("for.html", fruits=fruits)

@app.route("/if/<int:age>")
def if_(age: int):
  return render_template("if.html", age=age)

@app.route("/safe")
def safe():
  html: str = "<script>alert('Hacked !!!')</script>"
  return render_template("safe.html", html=html)

@app.route("/pandas")
def pandas_safe():
  df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
  return render_template("safe.html", html=df.to_html())


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8081, debug=True)