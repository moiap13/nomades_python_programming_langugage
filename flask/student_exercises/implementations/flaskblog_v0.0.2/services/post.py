import os, sys

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
sys.path.append(ROOT_DIR)

from repositories.post_firestore import PostRepository
from models.post import Post

class PostService():
  def __init__(self):
    self._repo = PostRepository()

  def get_all(self) -> list[Post]:
    return self._repo.get_all()

  def get_my(self, uid: str) -> list[Post]:
    return self._repo.get_my(uid)

  def create(self, post: Post) -> Post:
    # TODO: Summarize the post
    # Use AI to summarize the post
    return self._repo.create(post)