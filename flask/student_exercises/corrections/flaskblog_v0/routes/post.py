import os, sys
ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

import json

from flask import Blueprint, flash, redirect, render_template, request, session, url_for, Response

from helpers.decorators import authenticated
from repositories.post import PostRepository
from repositories.user import UserRepository
from models.post import Post
from models.user import User
from forms.post import CreatePostForm
from helpers.gemini import GeminiAssistantService

UPLOAD_DIR: str = os.path.join(ROOT_DIR, 'static', 'uploads')
PP_DIR: str = os.path.join(UPLOAD_DIR, 'pp')

with open(os.path.join(ROOT_DIR, "config", "creds.json")) as json_config:
    config: dict[str, str] = json.load(json_config)

post_bp = Blueprint('post', __name__, url_prefix='/post')
post_repository = PostRepository()
user_repository = UserRepository()
post_summarizer = GeminiAssistantService(
  config.get("gemini_api_key", ""), 
  "You are a online blog article reviwever, your role is to get the most important infomrations from the posts and summarize them without losing informations",
  "gemini-3.5-flash"
)

@post_bp.route("/get")
@authenticated
def get_all_posts() -> str:
  posts: list[Post] = post_repository.get_all()
  return render_template('post/list.html', posts=posts, page_title="All posts")

# Create the route /post/get/my
@post_bp.route("/get/my")
@authenticated
def get_my_posts() -> str:
  # This route get all the posts from the posts collection where the author is myself
  # to check if the author is myself, get all post where author == my user firestore document reference
  # Display all the matched posts in a page (you can modify post/list.html file or create a new one)
  posts: list[Post] = post_repository.get_my(session['firestore_id'])
  return render_template('post/list.html', posts=posts, page_title="All my posts") 

@post_bp.route("/create", methods=["GET", "POST"])
@authenticated
def create_post() -> str:
  form = CreatePostForm(request.form)

  if request.method == "POST" and form.validate():
    title: str = form.title.data
    body: str = form.body.data
    author: User = user_repository.get_by_firestore_id(session['firestore_id'])

    summary: str = post_summarizer.basic_chat(f"Please summyrize in one sentence this blog text: {body}")

    post: Post = Post(title=title, body=body, author=author, summary=summary)
    post = post_repository.create(post)

    flash(f"Post created successfully with id={post.id}", "success")
    return redirect(url_for('post.get_my_posts'))

  return render_template("post/create.html", form=form)

@post_bp.route("/delete/<post_id>")
@authenticated
def delete_post(post_id: str) -> Response:
  post: Post = post_repository.get_by_firestore_id(post_id)
  if not post.is_my(session["firestore_id"]):
    flash(f"You are not the authro of post with id={post_id}", "danger")
    return redirect(url_for('post.get_my_posts'))

  post_repository.delete(post_id)

  flash(f"Post with id={post_id} successfully deleted", "success")
  return redirect(url_for('post.get_my_posts'))
  
# TODO(bonus): Add view post, update post, deleted post