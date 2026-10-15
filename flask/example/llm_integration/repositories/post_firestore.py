import os, sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from firebase_admin import firestore

from config.firestore_connection import db
from models.post import Post
from models.user import User

from .user_firestore import get_user_by_firestore_id

class PostFirestoreRepository:
  def __init__(self, collection_name: str = "posts"):
    self.collection_name = collection_name
    self.collection_ref = db.collection(collection_name)

  def create(self, post: Post) -> Post:
    # get a post as paramater and create it in the firestore database
    # /!\ the user object should be transformed to a firestore reference
    post_data: dict[str, str | User | "datetime"] = post.to_dict()
    post_data["author"] = db.collection("users").document(post_data["author"].firestore_id)
    _, doc_ref = self.collection_ref.add(post_data)
    post.firestore_id = doc_ref.id
    return post

  def get_all(self) -> list[Post]:
    posts: list[Post] = []
    for post in self.collection_ref.get():
      post_data: dict = post.to_dict()
      post_data["author"] = get_user_by_firestore_id(post_data["author"].id, db)
      posts.append(Post.from_dict(post_data | {"firestore_id": post.id}))

    return posts

  def get_by_user(self, user: User) -> list[Post]:
    author_ref = db.collection("users").document(user.firestore_id)

    posts: list[Post] = []
    for post in self.collection_ref.where("author", "==", author_ref).get():
      post_data: dict = post.to_dict()
      post_data["author"] = user
      posts.append(Post.from_dict(post_data | {"firestore_id": post.id})) 
    
    return posts

  def delete(self, firestore_id: str) -> None:
    self.collection_ref.document(firestore_id).delete()

  def get_by_firestore_id(self, firestore_id: str) -> Post:
    post = self.collection_ref.document(firestore_id).get().to_dict()
    post["author"] = get_user_by_firestore_id(post["author"].id, db)
    return Post.from_dict(post | {"firestore_id": firestore_id})