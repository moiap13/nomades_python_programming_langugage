from flask import Flask

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return "<h1>Hello PPL 2026 0103 !!</h1><ul><li>Pomme</li><li>Banane</li></ul>"


@app.route("/hello")
def hello() -> str:
    return "<h1>Hello World</h1>"


@app.route("/hello/<name>")
def hello_name(name: str) -> str:
    return f"<h1>{name.capitalize()}</h1>"


@app.route("/hello/age/<int:age>")
def hello_age(age: int) -> str:
    return f"Age: <h1>{age}</h1>"


@app.route("/hello/age/<ages>")
def hello_ages(ages: int) -> str:
    return f"Ages: <h1>{ages}</h1>"


@app.route("/allow/<int:age>")
def allow_voting(age: int) -> str:
    return (
        "You are allowed to enter the voting website"
        if age >= 18
        else "You are not allowed to enter the voting website"
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
