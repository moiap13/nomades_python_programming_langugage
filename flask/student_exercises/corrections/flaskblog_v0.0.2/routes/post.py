# Create the post blueprint and add the necessary routes
# /!\ Don't forget to register the blueprint in the app server
import os, sys

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
sys.path.append(ROOT_DIR)

from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
import plotly.express as px
import pandas as pd

from helpers.decorators import authenticated

from forms.post import PostCreationForm
from models.post import Post
from models.user import User
from services.post import PostService
from services.user import UserService
from services.post_analysis import PostAnalysisService

post_bp = Blueprint('post', __name__, url_prefix='/post')

post_service = PostService()
user_service = UserService()
post_analysis_service = PostAnalysisService()

# Create post creation route
@post_bp.route("/create", methods=["GET", "POST"])
@authenticated
def create_post() -> str:
  form = PostCreationForm(request.form)

  if request.method == "POST" and form.validate():
    # Add post in database
    post = post_service.create(Post(
      title=form.title.data,
      body=form.body.data,
      author=User(
        firestore_id=session['firestore_id'],
        uid=session['uid'],
        firstname="",
        lastname="",
        email="",
      )
    ))

    flash(f"Post created successfully with id={post.firestore_id}", "success")
    return redirect(url_for('post.get_all_posts'))
    
  return render_template("post/create.html", form=form)

# Create get all posts of the system route
@post_bp.route("/all")
@authenticated
def get_all_posts() -> str:
  date_start = request.args.get('date_start')
  date_end = request.args.get('date_end')

  if date_start and date_end:
    posts: list[Post] = post_service.get_by_dates(datetime.strptime(date_start, "%Y-%m-%d"), datetime.strptime(date_end, "%Y-%m-%d"))
  else:
    posts: list[Post] = post_service.get_all()

  return render_template('post/list.html', posts=posts, page_title="All posts", user_service=user_service)

# Create get my posts route
@post_bp.route("/my")
@authenticated
def get_my_posts() -> str:
  posts: list[Post] = post_service.get_my(session['firestore_id'])
  return render_template('post/list.html', posts=posts, page_title="My posts", user_service=user_service)

@post_bp.route("/delete", methods=["POST"])
def delete():
  post_service.delete(request.form['post_id'])
  flash("Post deleted successfully", "success")
  return redirect(url_for('post.get_all_posts'))

@post_bp.route("/analysis")
def analysis():
  date_start = request.args.get('date_start')
  date_end = request.args.get('date_end')

  if date_start and date_end:
    posts: list[Post] = post_service.get_by_dates(datetime.strptime(date_start, "%Y-%m-%d"), datetime.strptime(date_end, "%Y-%m-%d"))
  else:
    posts: list[Post] = post_service.get_all()

  posts_per_date: pd.Series = post_analysis_service.get_posts_by_dates(posts)

  post_per_date_bar = px.bar(posts_per_date)

  return render_template(
    'post/analysis.html', 
    posts=posts,
    post_per_date_bar=post_per_date_bar.to_html(full_html=False, include_plotlyjs='cdn')
  )

@post_bp.route("/get/<author_id>")
@authenticated
def get_by_author(author_id: str) -> str:
  posts: list[Post] = post_service.get_by_author_firestore_id(author_id)
  author: User = user_service.get_user_by_firestore_id(author_id) # type: User
  return render_template('post/list.html', posts=posts, page_title=f"{author.uid}'s posts", user_service=user_service)

@post_bp.route("/analysis/streamilit")
def analysis_iframe():
  return render_template('post/analysis_iframe.html')