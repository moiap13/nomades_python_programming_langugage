# Add post database interractions
import os, sys

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
sys.path.append(ROOT_DIR)

from firebase_admin import firestore

from config.firestore_config import db
from models.post import Post

class PostRepository:
  def __init__(self, collection_name: str="posts"):
    self.collection_name = collection_name
    self.collection_ref = db.collection(collection_name)

  def create(self, post: Post) -> Post:
    """
    Function used to add a new post to the database

    Parameters
    ----------
    post : Post
        Post to add to the database

    Returns
    -------
    Post 
        Post added to the database including the firestore id
    """
    _, doc_ref = self.collection_ref.add(post.to_dict())
    post.firestore_id = doc_ref.id
    return post

  def get_all(self) -> list[Post]:
    post_snapshots = self.collection_ref.order_by("created_at", direction=firestore.Query.DESCENDING).get()
    posts: list[Post] = [
      Post.from_dict(post_snapshot.to_dict() | {"firestore_id": post_snapshot.id}) 
      for post_snapshot in post_snapshots
    ]

    return posts

  def get_my(self, uid: str) -> list[Post]:
    post_snapshots = self.collection_ref.where("author", "==", uid).order_by("created_at", direction=firestore.Query.DESCENDING).get()
    posts: list[Post] = [
      Post.from_dict(post_snapshot.to_dict() | {"firestore_id": post_snapshot.id}) 
      for post_snapshot in post_snapshots
    ]

    return posts
