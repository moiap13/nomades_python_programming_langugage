from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
  return "Index"

@app.route("/coucou")
def salut():
  return "Bonjour"

@app.route("/coucou/<name>/<int:age>")
def text(name: str, age: int):
  print(type(name), type(age))
  return f"Bonjour {name} vous avez {age} années"

@app.route("/response/html")
def html():
  name = "Antonio"
  return f"""
    <h1>Bonjour {name}</h1>
    <ol>
      <li><h2>Banana</h2></li>
      <li><h2>Apple</h2></li>
      <li><h2>Watermelon</h2></li>
      <li><h2>Strawberry</h2></li>
      <li><h2>Peach</h2></li>
    </ol>
  """

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8081, debug=True)
