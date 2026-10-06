from flask import Flask

app = Flask(__name__)

@app.route("/")
def index() -> str:
  return '<h1>Hello PPL 2026 3T2, from <span style="color: red;">nomades</span> class</h1>'

@app.route('/allow/<int:age>')
def allow_voting(age: int) -> str:
    return (
       "You are allowed to enter the voting website" 
       if age >= 18 
       else "You are not allowed to enter the voting website"
    )

@app.route('/allow/<age>')
def allow_voting_str(age: str) -> str:
    return f"Your string value is {age}"

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8000, debug=True)
  #localhost