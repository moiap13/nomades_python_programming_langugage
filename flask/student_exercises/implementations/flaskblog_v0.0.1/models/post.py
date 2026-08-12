class Post():
  def __init__(self, title: str, body: str, author: str, firestore_id: str = "", created_at: str = "", updated_at: str = ""):
    self.firestore_id = firestore_id
    self.title = title
    self.body = body
    self.author = author # store the uid of the author
    self.created_at = created_at
    self.updated_at = updated_at

  @staticmethod
  def from_dict(source: dict[str, str]):
    return Post(source["title"], source["body"], source["author"], source["firestore_id"], source["created_at"], source["updated_at"])

  def to_dict(self, include_id: bool = False) -> dict[str, str]:
    return {
      "title": self.title,
      "body": self.body,
      "author": self.author,
      "created_at": self.created_at,
      "updated_at": self.updated_at
    } | ({"firestore_id": self.firestore_id} if include_id else {})