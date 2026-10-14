import os, sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config.firestore_connection import db
from models.post import Post
from models.user import User

from .user_firestore import get_user_by_firestore_id

class PostFirestoreRepository:
  def __init__(self, collection_name: str = "posts"):
    self.collection_name = collection_name
    self.collection_ref = db.collection(collection_name)

  def create(self, post: Post) -> Post:
    user_doc_ref = db.collection("users").document(post.author.firestore_id)
    _, doc_ref = self.collection_ref.add(post.to_dict() | {"author": user_doc_ref})
    post.firestore_id = doc_ref.id
    return post

  def get_all(self) -> list[Post]:
    posts: list[Post] = []
    
    for post in self.collection_ref.get():
      post_data: dict = post.to_dict()
      post_data["author"] = get_user_by_firestore_id(post_data["author"].id, db)
      posts.append(Post.from_dict(post_data))

    return posts

  def get_by_user(self, user: User) -> list[Post]:
    author_ref = db.collection("users").document(user.firestore_id)

    posts: list[Post] = []
    for post in self.collection_ref.where("author", "==", author_ref):
      post_data: dict = post.to_dict()
      post_data["author"] = user
      posts.append(Post.from_dict(post_data)) 
    
    return posts