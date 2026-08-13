# Create the post blueprint and add the necessary routes
# /!\ Don't forget to register the blueprint in the app server
import os, sys

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
sys.path.append(ROOT_DIR)

from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from helpers.decorators import authenticated

from forms.post import PostCreationForm
from models.post import Post
from services.post import PostService
from services.user import UserService

post_bp = Blueprint('post', __name__, url_prefix='/post')

post_service = PostService()
user_service = UserService()

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
      author=session["uid"],
      created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ))

    flash(f"Post created successfully with id={post.firestore_id}", "success")
    return redirect(url_for('post.get_all_posts'))
    
  return render_template("post/create.html", form=form)

# Create get all posts of the system route
@post_bp.route("/all")
@authenticated
def get_all_posts() -> str:
  posts: list[Post] = post_service.get_all()
  return render_template('post/list.html', posts=posts, page_title="All posts", user_service=user_service)

# Create get my posts route
@post_bp.route("/my")
@authenticated
def get_my_posts() -> str:
  posts: list[Post] = post_service.get_my(session['uid'])
  return render_template('post/list.html', posts=posts, page_title="My posts", user_service=user_service)