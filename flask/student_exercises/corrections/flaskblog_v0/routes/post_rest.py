import os, sys
ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from flask import Blueprint, flash, redirect, render_template, request, session, url_for, jsonify

from helpers.decorators import authenticated
from repositories.post import PostRepository
from repositories.user import UserRepository
from models.post import Post
from models.user import User
from forms.post import CreatePostForm


UPLOAD_DIR: str = os.path.join(ROOT_DIR, 'static', 'uploads')
PP_DIR: str = os.path.join(UPLOAD_DIR, 'pp')

post_bp_rest = Blueprint('api_post', __name__, url_prefix='/api/post')
post_repository = PostRepository()
user_repository = UserRepository()

@post_bp_rest.route("/get")
@authenticated
def api_get_all_posts() -> str:
  posts: list[Post] = post_repository.get_all()
  return jsonify({'posts': [post.to_json() for post in posts]}), 200
