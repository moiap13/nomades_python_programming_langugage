import os, sys

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)

sys.path.append(ROOT_DIR)

from datetime import datetime

from models.user import User


class Article:
    def __init__(
        self,
        id: str,
        title: str,
        body: str,
        authors: list[User],
        body_summury: str = "",
        last_modify: datetime = datetime.now(),
        created_at: datetime = datetime.now(),
    ) -> None:
        self.id = id
        self.title = title
        self.body = body
        self.authors = authors
        self.body_summury = body_summury
        self.last_modify = last_modify
        self.created_at = created_at

    def __str__(self) -> str:
        return f"Article({self.id}, {self.title})"

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def from_dict(source: dict[str, str | User]) -> "Article":
        return Article(
            id=source.get("id", ""),
            title=source.get("title", ""),
            body=source.get("body", ""),
            authors=source.get("authors", ""),
            body_summury=source.get("body_summury", ""),
            last_modify=source.get("last_modify", None),
            created_at=source.get("created_at", datetime.now()),
        )

    def to_dict(
        self, include_id: bool = False
    ) -> dict[str, str | list[dict[str, str]]]:
        return {
            "title": self.title,
            "body": self.body,
            "body_summury": self.body_summury,
            "authors": [user.to_dict(include_id=True) for user in self.authors],
            "last_modify": self.last_modify,
            "created_at": self.created_at,
        } | ({"id": self.id} if include_id else {})

    def is_user_author(self, user: User) -> bool:
        return user.id in [author.id for author in self.authors]
