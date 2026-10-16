import os

from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import folium
import requests

app = Flask(__name__)

ROOT_DIR = os.path.dirname(__file__)
POSTS_CSV = os.path.join(ROOT_DIR, "data", "posts.csv")


@app.route("/")
def index():
    return "Hello World!"


@app.route("/post/day")
def post_per_day():
    df = pd.read_csv(POSTS_CSV)
    df.created_at = pd.to_datetime(df["created_at"]).dt.date

    post_per_day = df.groupby("created_at").size()
    post_per_date_bar = px.bar(post_per_day)

    post_per_authors_and_date = df.groupby(["created_at", "author"]).size()
    post_per_authors_date_bar = px.bar(
      post_per_authors_and_date, 
      x=post_per_authors_and_date.index.get_level_values(0), 
      y=post_per_authors_and_date.values, 
      color=post_per_authors_and_date.index.get_level_values(1)
    )

    post_per_date_cumsum = post_per_day.cumsum()
    cumsum_plot = px.line(post_per_date_cumsum)

    return render_template(
        "stats/post_per_day.html",
        post_per_day_bar=post_per_date_bar.to_html(include_plotlyjs="cdn", full_html=False),
        post_per_author_day_bar=post_per_authors_date_bar.to_html(
            full_html=False, include_plotlyjs=False
        ),
        post_per_date_cumsum=cumsum_plot.to_html(
            full_html=False, include_plotlyjs=False
        ),
        df=df.to_html(classes="table table-striped"),
    )

@app.route("/post/author/location")
def post_per_author_location():
  m = folium.Map(location=(45.5236, -122.6750))
  users: list[dict] = requests.get('https://jsonplaceholder.typicode.com/users').json()

  for user in users:  
    lat = float(user["address"]["geo"]["lat"])
    lng = float(user["address"]["geo"]["lng"])

    popup = render_template('components/popup_content.html', user=user)

    folium.Marker([lat, lng], popup=popup, tooltip=user['email']).add_to(m)

  return render_template("user/userloc.html", userloc_map=m._repr_html_(), users=users)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
