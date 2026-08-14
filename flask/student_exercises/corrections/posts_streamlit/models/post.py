import os, sys

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
sys.path.append(ROOT_DIR)

from datetime import datetime

from models.user import User

class Post():
  def __init__(self, title: str, body: str, author: User, summary: str = "", firestore_id: str = "", created_at: datetime = datetime.now(), updated_at: datetime = datetime.now()):
    self.firestore_id = firestore_id
    self.title = title
    self.body = body
    self.summary = summary
    self.author = author # self.author store a User object
    self.created_at = created_at
    self.updated_at = updated_at

  @staticmethod
  def from_dict(source: dict[str, str]):
    return Post(source["title"], source["body"], source["author"], source["summary"], source["firestore_id"], source["created_at"], source["updated_at"])

  def to_dict(self, include_id: bool = False) -> dict[str, str]:
    return {
      "title": self.title,
      "body": self.body,
      "author": self.author.to_dict(),
      "summary": self.summary,
      "created_at": self.created_at,
      "updated_at": self.updated_at
    } | ({"firestore_id": self.firestore_id} if include_id else {})

  def is_author(self, author: str | User) -> bool:
    return self.author == author
