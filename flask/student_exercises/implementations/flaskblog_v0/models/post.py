from datetime import datetime

from .user import User


class Post:
  def __init__(self, id: str="", title: str="", body: str="", author: User=None, created_at: datetime=datetime.now()):
    self.id = id
    self.title = title
    self.body = body
    self.author = author
    self.created_at = created_at
  
  @staticmethod
  def from_dict(source: dict[str, str | User | datetime]) -> "Post":
    return Post(
      id=source.get("id", ""),
      title=source.get("title", ""),
      body=source.get("body", ""),
      author=source.get("author", None),
      created_at=source.get("created_at", None)
    )
  
  def to_dict(self) -> dict[str, str | User]:
    return {
      "id": self.id,
      "title": self.title,
      "body": self.body,
      "author": self.author,
      "created_at": self.created_at
    }
  
  def __str__(self) -> str:
    return f"Post(id={self.id}, {self.title})"

  def __repr__(self) -> str:
    return self.__str__()