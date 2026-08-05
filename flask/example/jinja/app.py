from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__, template_folder='src')

@app.route('/')
def index() -> str:
  return render_template('index.html')

@app.route("/var")
def var() -> str:
  firstname: str = "Antonio"
  lastname: str = "Pisanello"
  return render_template("var.html", name=firstname, ln=lastname)
@app.route("/var/<firstname>/<lastname>")

def var_dyn(firstname: str, lastname:str) -> str:
  return render_template("var.html", name=firstname, ln=lastname)

@app.route("/for")
def jinja_for():
  fruits: list[str] = [
    "apple",
    "banana",
    "orange",
    "kiwi",
    "grape",
    "pear",
    "peach",
    "plum",
    "cherry",
    "strawberry",
  ]

  return render_template("control_structures/for.html", fruits=fruits)

@app.route("/if/<int:age>")
def jinja_if(age: int):
  return render_template("control_structures/if.html", age=age)

@app.route("/filter")
def jinja_filter():
  firstname: str = "anToNIo"
  lastname: str = "PisANelLo"

  comment: str = "<script>alert('Hacked');</script>"

  df = pd.DataFrame(
    {
      "Name": ["Antonio", "Marcelo", "Samuele"],
      "Age": [20, 21, 22],
      "City": ["Rome", "Milan", "<scipt>alert('Hacked');</script>"],
    }
  )

  plot = px.bar(df, x="Name", y="Age", color="City", barmode="group")
  
  return render_template("filter.html", 
    fn=firstname, 
    ln=lastname, 
    comment=comment, 
    df_table=df.to_html(classes='table table-striped', index=False),
    plot_html=plot.to_html(full_html=False, include_plotlyjs='cdn')
  ) 

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)