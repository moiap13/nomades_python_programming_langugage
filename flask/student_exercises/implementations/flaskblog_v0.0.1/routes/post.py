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

#TODO: Create get my posts route
# The route is accessible using GET in /posts/my
# this route will show all the posts from the posts collection where the author is myself
# You get the authors firestore id from the session
# This route render the post/list.html template

#TODO: Create route for creating a new post
# This route is accessible using GET in /posts/create
# This route render the post/create.html template
# This route accepts a POST request, with a form containing a title and a body
# This route should create a new post in the posts firestore collection, 
#   witht the authors id the connected firestore user id

# TODO: These twos rroutes must be protected