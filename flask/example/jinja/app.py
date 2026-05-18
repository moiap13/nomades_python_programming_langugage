from flask import Flask, render_template
import pandas as pd

app = Flask(__name__, template_folder="src")

@app.route("/")
def index() -> str:
  return render_template('index.html')

@app.route("/variable")
def variable():
  n: str = "Mamy"
  ln: str = "Pisanello"
  return render_template("variable.html", firstname=n, lastname=ln)

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

  return render_template("for.html", fruits=fruits)

@app.route("/if")
def jinja_if():
  age = 16
  return render_template("if.html", age=age)

@app.route("/safe")
def jinja_safe():
  comment: str = '<script>alert("Hacked!!!")</script>' # XSS attack
  return render_template("safe.html", comment=comment)

@app.route("/df")
def df() -> str:
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    df_html = df.to_html()
    return render_template("df.html", df_html=df_html)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
