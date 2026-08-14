# Add post database interractions
from datetime import datetime
import os, sys

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
sys.path.append(ROOT_DIR)

from firebase_admin import firestore

from config.firestore_config import db
from models.post import Post

from .users_firestore import UserRepository
from exceptions.user import UserNotFoundError

class PostRepository:
  def __init__(self, collection_name: str="posts"):
    self.collection_name = collection_name
    self.collection_ref = db.collection(collection_name)
    self.user_repository = UserRepository()

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
    _, doc_ref = self.collection_ref.add(post.to_dict() | {"author": db.collection("users").document(post.author.firestore_id)})
    post.firestore_id = doc_ref.id
    return post

  def get_all(self) -> list[Post]:
    post_snapshots = self.collection_ref.order_by("created_at", direction=firestore.Query.DESCENDING).get()
    posts: list[Post] = [
      Post.from_dict(post_snapshot.to_dict() | {
        "firestore_id": post_snapshot.id,
        "author": self.user_repository.get_user_by_firestore_id(post_snapshot.to_dict()["author"].id)
      }) 
      for post_snapshot in post_snapshots
    ]

    return posts

  def get_by_author_firestore_id(self, firestore_id: str) -> list[Post]:
    author_ref = db.collection("users").document(firestore_id)
    post_snapshots = self.collection_ref.where("author", "==", author_ref).order_by("created_at", direction=firestore.Query.DESCENDING).get()
    posts: list[Post] = [
      Post.from_dict(post_snapshot.to_dict() | {
        "firestore_id": post_snapshot.id, 
        "author": self.user_repository.get_user_by_firestore_id(post_snapshot.to_dict()["author"].id)
      }) 
      for post_snapshot in post_snapshots
    ]

    return posts

  def get_by_uid(self, uid: str) -> list[Post]:
      try:
        author = self.user_repository.get_user_by_uid(uid)
      except UserNotFoundError:
        return []

      return self.get_by_author_firestore_id(author.firestore_id)

  def get_my(self, firestore_id: str) -> list[Post]:
    return self.get_by_author_firestore_id(firestore_id)

  def delete(self, firestore_id: str) -> None:
    print(firestore_id)
    self.collection_ref.document(firestore_id).delete()

  def get_by_dates(self, start_date: datetime, end_date: datetime) -> list[Post]:
    return [
      Post.from_dict(post_snapshot.to_dict() | {
        "firestore_id": post_snapshot.id, 
        "author": self.user_repository.get_user_by_firestore_id(post_snapshot.to_dict()["author"].id)
      }) 
      for post_snapshot in self.collection_ref.where("created_at", ">=", start_date).where("created_at", "<=", end_date).get()
    ]
