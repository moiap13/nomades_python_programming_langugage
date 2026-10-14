import os, sys
ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from flask import Blueprint, render_template

from models.post import Post
from repositories.post_firestore import PostFirestoreRepository


post_bp = Blueprint("post", __name__, url_prefix="/posts")

post_repo = PostFirestoreRepository()

@post_bp.route("/")
def get_all():
  posts: list[Post] = post_repo.get_all()
  return render_template('post/list_posts.html', posts=posts)