import os, sys
ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from datetime import datetime

from config.firestore_connection import DocumentReference, DocumentSnapshot
from repositories.user import UserRepository
from models.post import Post

class PostMapper():
  def __init__(self):
    self.user_repository = UserRepository()
  
  def to_post(self, source: dict | DocumentReference | DocumentSnapshot) -> Post:
    if type(source) == DocumentReference:
      source = source.get()
    if type(source) == DocumentSnapshot:
      source = source.to_dict() | {"id": source.id}
      source["author"] = self.user_repository.get_by_firestore_id(source["author"].id)
      source["created_at"] = datetime.fromtimestamp(source["created_at"].timestamp())
    if type(source) == dict:
      # source = Post(
      #   id=source.get("id", ""),
      #   title=source.get("title", ""),
      #   body=source.get("body", ""),
      #   author=source.get("author", None),
      #   created_at=source.get("created_at", None)
      # )
      source = Post.from_dict(source)
  
    return source

  # def to_dict(self, post: Post) -> dict[str, str | User]:
  #   return {
  #     "id": post.id,
  #     "title": post.title,
  #     "body": post.body,
  #     "author": post.author,
  #     "created_at": post.created_at
  #   }

  # def to_json(self) -> dict[str, str | dict[str, str]]:
  #   return {
  #     "id": self.id,
  #     "title": self.title,
  #     "body": self.body,
  #     "author": self.author.to_dict(),
  #     "created_at": self.created_at
  #   } 