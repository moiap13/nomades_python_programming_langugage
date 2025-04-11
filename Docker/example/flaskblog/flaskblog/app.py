import os
import json

CURR_DIR = os.path.dirname(__file__)
CONFIG_FILE_PATH = os.path.join(CURR_DIR, "config", "server-creds.json")

from flask import Flask, render_template, session, redirect, url_for, flash
from firebase_admin.firestore import DocumentSnapshot, DocumentReference, SERVER_TIMESTAMP
from firebase_admin import firestore

import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import plotly.express as px

from config.firestore_connection import db

from src.login.login_bp import login_bp
from src.posts.posts_bp import post_bp
from helpers.decorators import authenticated

with open(CONFIG_FILE_PATH, "r") as json_config:
  config = json.load(json_config)
  
app = Flask(__name__)
app.config["SECRET_KEY"] = config["SECRET_KEY"]

app.register_blueprint(login_bp)
app.register_blueprint(post_bp)

@app.route("/userinfo")
@authenticated
def userinfo():
  # Get the user infos from the session and pass them to the template
  return render_template("user/user_info.html", user=session["user"])

@app.route("/")
def index():
  # DATA PREPARATION
  posts = db.collection("random_posts").get()

  data_dict: list[dict] = []
  for doc in posts:
    doc_dict = doc.to_dict()
    authors_names: list[str] = []
    for author in doc_dict["authors"]:
      author_dict = author.get().to_dict()
      authors_names.append(f"{author_dict.get('firstname', 'Unammed')} {author_dict.get('lastname', 'Unammed')}")
    doc_dict["authors"] = ";".join(authors_names)
    data_dict.append(doc_dict)
  data_dict

  df = pd.DataFrame(data_dict)

  # DATA TRANSFORMATION
  df["created_at"] = pd.to_datetime(df["created_at"])
  df["date"] = df["created_at"].dt.date

  # ONE HOT ENCODING for authors
  authors: list[str] = []

  def authors_map(author_s: str):
    for author in author_s.split(";"):
      authors.append(author)

  df.authors.map(authors_map)

  unique_authors = set(authors)
  unique_authors

  for author in unique_authors:
    df[author] = df.authors.map(lambda author_s_l: int(author in author_s_l))

  # DATA ANALYSIS
  post_counts = df.groupby("date").size().reset_index(name="post_counts")
  
  # plt.plot(post_counts.date, post_counts.post_counts)
  # plt.xticks(rotation=45)
  # plt.savefig(os.path.join(CURR_DIR, "static", "plots", "post_per_date_line.png"))
  # plt.close()
  # plt.bar(post_counts.date, post_counts.post_counts)
  # plt.xticks(rotation=45)
  # plt.savefig(os.path.join(CURR_DIR, "static", "plots", "post_per_date_bar.png"))
  # plt.close()

  post_date_count_line = px.line(post_counts, x="date", y="post_counts")
  post_date_count_bar = px.bar(post_counts, x="date", y="post_counts")


  return render_template(
    "index_plotly.html", 
    data=df.to_html(classes="table table-hover table-stripped"),
    post_date_count_line=post_date_count_line.to_html(full_html=False),
    post_date_count_bar=post_date_count_bar.to_html(full_html=False)
  )


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8081, debug=True)