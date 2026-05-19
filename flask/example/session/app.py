from flask import Flask, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "superstrongpassword"

@app.route("/counter")
def counter() -> str:
  if "counter" in session:
    session["counter"] += 1
  else:
    session["counter"] = 1

  return f"Counter value: {session["counter"]}"

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True)
