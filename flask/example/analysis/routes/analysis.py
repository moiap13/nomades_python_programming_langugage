import os, sys
ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from datetime import datetime

from flask import Blueprint, render_template, request, url_for
import folium
import pandas as pd
import plotly.express as px

from helpers.decorators import authenticated
from repositories.post import PostRepository
from repositories.user import UserRepository
from models.post import Post
from models.user import User
from forms.analysis import AnalysisForm

UPLOAD_DIR: str = os.path.join(ROOT_DIR, 'static', 'uploads')
PP_DIR: str = os.path.join(UPLOAD_DIR, 'pp')

analysis_bp = Blueprint("analysis", __name__)

post_repository = PostRepository()
user_repository = UserRepository()

@analysis_bp.route("/map")
@authenticated
def map() -> str:
  posts: list[Post] = [post for post in post_repository.get_all() if post.latlng != {}]
  m = folium.Map(location=(46.2044,6.1432), zoom_start=10)
  
  for post in posts:
    user: User = user_repository.get_by_firestore_id(post.author.id)

    if user.pp_exits(PP_DIR):
      user_pp = url_for('static', filename=f'uploads/pp/{user.pp_filename}')
    else:
      user_pp = user.get_pp_ui_avatars_src()
      
    folium.Marker(
      location=[post.latlng["lat"], post.latlng["lng"]],
      popup=render_template(
        'analysis/components/post_marker_popup.html',
        ID=post.id, 
        author_name=post.author.get_full_name(), 
        summary=post.summary, 
        user_pp=user_pp
      ),
      tooltip=post.id
    ).add_to(m)

    m.fit_bounds(m.get_bounds(), padding=(30, 30))

  return render_template('analysis/map.html', map_html=m._repr_html_())

@analysis_bp.route("/authors", methods=["GET", "POST"])
@authenticated
def authors() -> str:
  form = AnalysisForm(request.form)
  
  posts: list[Post] = post_repository.get_all()
  # TODO: remove duplicates
  authors: list[User] = [post.author for post in posts]

  form.authors.choices = [(author.id, author.get_full_name()) for author in authors]
  form.authors.default = [author.id for author in authors]

  form.start_date.choices = [(post.created_at.strftime("%Y-%m-%d"), post.created_at.strftime("%Y-%m-%d")) for post in posts]
  form.start_date.default = sorted(form.start_date.choices)[0][0]
  
  form.end_date.choices = [(post.created_at.strftime("%Y-%m-%d"), post.created_at.strftime("%Y-%m-%d")) for post in posts]
  form.start_date.default = sorted(form.start_date.choices)[-1][0]

  if request.method == "POST" and form.validate():
    selected_authors_ids: list[str] = form.authors.data
    selected_start_date: str = form.start_date.data
    selected_end_date: str = form.end_date.data

    authors: list[User] = [user_repository.get_by_firestore_id(author_id) for author_id in selected_authors_ids]
    start_date: datetime = datetime(*[int(s) for s in selected_start_date.split('-')])
    end_date: datetime = datetime(*[int(s) for s in selected_end_date.split('-')])

    posts: list[Post] = post_repository.get_analysis(authors, start_date, end_date)
    posts_dict: list[dict[str, str]] = [{
      "title": post.title,
      "body": post.body,
      "author": post.author.get_full_name(),
      "created_at": post.created_at.strftime("%Y-%m-%d")
    } for post in posts]
    posts_dataframe = pd.DataFrame(posts_dict)

    post_per_date: pd.Series = posts_dataframe.groupby("created_at").size()
    post_per_date_bar = px.bar(post_per_date)

    post_per_authors_and_date = posts_dataframe.groupby(["created_at", "author"]).size()
    post_per_authors_date_bar = px.bar(
        post_per_authors_and_date,
        x=post_per_authors_and_date.index.get_level_values(0),
        y=post_per_authors_and_date.values,
        color=post_per_authors_and_date.index.get_level_values(1),
    )


    return render_template(
      'analysis/authors.html', 
      form=form, 
      selected_authors_ids=selected_authors_ids, 
      selected_start_date=selected_start_date, 
      selected_end_date=selected_end_date,
      post_per_date_bar_html=post_per_date_bar.to_html(full_html=False),
      post_per_authors_date_bar_html=post_per_authors_date_bar.to_html(include_plotlyjs=False, full_html=False)
    )


  return render_template('analysis/authors.html', form=form)