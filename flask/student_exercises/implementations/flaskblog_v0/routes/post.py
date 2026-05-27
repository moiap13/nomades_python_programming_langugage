import os, sys
ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from helpers.decorators import authenticated
from repositories.post import PostRepository
from repositories.user import UserRepository
from models.post import Post
from models.user import User
from forms.post import CreatePostForm


UPLOAD_DIR: str = os.path.join(ROOT_DIR, 'static', 'uploads')
PP_DIR: str = os.path.join(UPLOAD_DIR, 'pp')

post_bp = Blueprint('post', __name__, url_prefix='/post')
post_repository = PostRepository()
user_repository = UserRepository()

@post_bp.route("/get")
@authenticated
def get_all_posts() -> str:
  posts: list[Post] = post_repository.get_all() + post_repository.get_all() 
  return render_template('post/list.html', posts=posts)

# TODO: Create the route /post/get/my
# This route get all the posts from the posts collection where the author is myself
# to check if the author is myself, get all post where author == my user firestore document reference
# TODO: Display all the matched posts in a page (you can modify post/list.html file or create a new one)

@post_bp.route("/create", methods=["GET", "POST"])
@authenticated
def create_post() -> str:
  form = CreatePostForm(request.form)

  if request.method == "POST" and form.validate():
    title: str = form.title.data
    body: str = form.body.data
    author: User = user_repository.get_by_firestore_id(session['firestore_id'])

    post: Post = Post(title=title, body=body, author=author)
    post = post_repository.create(post)

    flash(f"Post created successfully with id={post.id}", "success")
    return redirect(url_for('post.get_all_posts'))

  return render_template("post/create.html", form=form)
  
# TODO(bonus): Add view post, update post, deleted post