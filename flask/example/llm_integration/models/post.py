from datetime import datetime

from .user import User

class Post:
  def __init__(
    self, 
    firestore_id: str = "",
    title: str = "",
    body: str = "",
    summary: str = "",
    author: User | None = None,
    created_at: datetime = datetime.now()
  ):
    self.firestore_id = firestore_id
    self.title = title
    self.body = body
    self.summary = summary
    self.author = author
    self.created_at = created_at

  def to_dict(self, include_id: bool = False) -> dict[str, str | User | datetime]:
    return {
      "title": self.title,
      "body": self.body,
      "summary": self.summary,
      "author": self.author,
      "created_at": self.created_at
    } | ({"firestore_id": self.firestore_id} if include_id else {})

  def is_author(self, user: User) -> bool:
    return self.author.firestore_id == user.firestore_id

  @staticmethod
  def from_dict(source: dict[str, str | User | datetime]) -> "Post":
    return Post(
      firestore_id=source.get("firestore_id", ""),
      title=source.get("title", ""),
      body=source.get("body", ""),
      summary=source.get("summary", ""),
      author=source.get("author", None),
      created_at=source.get("created_at", datetime.now()) # TODO: make sure .now() is the correct behavior
    )