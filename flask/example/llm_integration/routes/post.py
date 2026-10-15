import json
import os, sys
ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from flask import Blueprint, flash, render_template, session, request, redirect, url_for

from AI.gemini import GoogleAIProvider
from config.firestore_connection import db
from forms.posts import CreatePostForm
from helpers.decorators import authenticated
from models.post import Post
from models.user import User
from repositories.post_firestore import PostFirestoreRepository
from repositories.user_firestore import get_user_by_firestore_id

post_bp = Blueprint("post", __name__, url_prefix="/posts")

with open(os.path.join(ROOT_DIR, "config", "creds.json")) as json_config:
  config: dict[str, str] = json.load(json_config)

post_repo = PostFirestoreRepository()
ai_assistant = GoogleAIProvider(config["gemini_api_key"], model_name="gemini-3.8-flash")

@post_bp.route("/")
def get_all():
  posts: list[Post] = post_repo.get_all()
  current_user: User = get_user_by_firestore_id(session["firestore_id"], db)
  return render_template('post/list_posts.html', posts=posts, title="All Posts", current_user=current_user)

#Create get my posts route
# The route is accessible using GET in /posts/my
# this route will show all the posts from the posts collection where the author is myself
# You get the authors firestore id from the session
# This route render the post/list.html template
@post_bp.route("/my")
@authenticated
def get_my_posts() -> str:
  current_user: User = get_user_by_firestore_id(session["firestore_id"], db)
  posts: list[Post] = post_repo.get_by_user(current_user)
  return render_template('post/list_posts.html', posts=posts, title="My Posts", current_user=current_user)

# Create route for creating a new post
# This route is accessible using GET in /posts/create
# This route render the post/create.html template
# This route accepts a POST request, with a form containing a title and a body
# This route should create a new post in the posts firestore collection, 
#   witht the authors id the connected firestore user id
@post_bp.route("/create", methods=["GET", "POST"])
@authenticated
def create():
  form = CreatePostForm(request.form)
  if request.method == "POST" and form.validate():
    # add post to database
    post = Post(
      title=form.title.data,
      body=form.body.data,
      summary=ai_assistant.generate_text(f"""
You are a internet blog chief editor.
This is a new blog post: 
{form.body.data}

I want you to summarize in one sentence.
      """),
      author=get_user_by_firestore_id(session["firestore_id"], db)
    )
    post = post_repo.create(post)

    flash(f"Post created successfully with id={post.firestore_id}", "success")
    
    # redirect to get my posts
    return redirect(url_for("post.get_my_posts"))
  return render_template("post/add_post.html", form=form)

# These twos rroutes must be protected

@post_bp.route("/delete", methods=["POST"])
@authenticated
def delete():
  current_user: User = get_user_by_firestore_id(session["firestore_id"], db)
  post = post_repo.get_by_firestore_id(request.form['post_id'])

  if not post.is_author(current_user):
    flash("You are not authorized to delete this post", "danger")
    return redirect(url_for('post.get_my_posts'))

  post_repo.delete(request.form['post_id'])
  flash("Post deleted successfully", "success")
  return redirect(url_for('post.get_my_posts'))