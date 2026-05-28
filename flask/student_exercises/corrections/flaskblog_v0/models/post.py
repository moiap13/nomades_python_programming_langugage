from datetime import datetime

from .user import User


class Post:
  def __init__(self, id: str="", title: str="", body: str="", summary: str="", latlng: dict[str, float]={}, author: User=None, created_at: datetime=datetime.now()):
    self.id = id
    self.title = title
    self.body = body
    self.summary = summary
    self.latlng = latlng
    self.author = author
    self.created_at = created_at
  
  @staticmethod
  def from_dict(source: dict[str, str | User | datetime]) -> "Post":
    return Post(
      id=source.get("id", ""),
      title=source.get("title", ""),
      body=source.get("body", ""),
      summary=source.get("summary", ""),
      latlng=source.get("latlng", {}),
      author=source.get("author", None),
      created_at=source.get("created_at", None)
    )
  
  def to_dict(self) -> dict[str, str | User]:
    return {
      "id": self.id,
      "title": self.title,
      "body": self.body,
      "summary": self.summary,
      "latlng": self.latlng,
      "author": self.author,
      "created_at": self.created_at
    }
  
  def to_json(self) -> dict[str, str | dict[str, str]]:
    return {
      "id": self.id,
      "title": self.title,
      "body": self.body,
      "summary": self.summary,
      "latlng": self.latlng,
      "author": self.author.to_dict(),
      "created_at": self.created_at
    } 
  
  def __str__(self) -> str:
    return f"Post(id={self.id}, {self.title} {self.author.get_full_name()})"

  def __repr__(self) -> str:
    return self.__str__()
  
  def is_my(self, author_id: str) -> bool:
    """
    Check if the gioven author id is the author of the post
    """
    return self.author.id == author_id