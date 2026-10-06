from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)

@app.route("/")
def index() -> str:
  return render_template("index.html")

@app.route("/variable")
def variable():
  name = "Anto"
  lastname = "Pisa"
  return render_template("variable.html", name=name, lastname=lastname)

@app.route("/variable/<name>/<lastname>")
def variable_dyn(name: str, lastname: str) -> str:
  return render_template("variable.html", name=name, lastname=lastname)

@app.route("/for")
def jinja_for():
  fruits = [
    "apple",
    "banana",
    "orange",
    "watermelon",
    "peach",
    "strawberry",
    "pinaple",
    "mango",
    "papaya",
    "lemon",
    "lime",
    "grape",
    "cherry",
    "raspberry",
  ]

  return render_template("for.html", fruits=fruits)

@app.route("/if")
def jinja_if():
  age = 20
  return render_template("if.html", age=age)

@app.route("/if/<int:age>")
def jinja_if_dynamic(age):
  return render_template("if.html", age=age)

@app.route("/safe") # XSS
def jinja_safe():
  html: str = '<script>alert("Hacked!!!")</script>'
  return render_template("safe.html", html=html)

@app.route("/safe/pd") # XSS
def jinja_safe_pd():
  df = pd.DataFrame({"name": ["John", "Jane", "Alice"], "email": ["john@example.com", "jane@example.com", "alice@example.com"]})
  return render_template("safe.html", html=df.to_html())

@app.route("/safe/plotly") # XSS
def jinja_safe_plotly():
  df = pd.DataFrame({"Year": [2010, 2011, 2012], "Sales": [100, 150, 200]})
  fig = px.bar(df, x="Year", y="Sales")
  return render_template("safe.html", html=fig.to_html(full_html=False))

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8000, debug=True)
  #localhost