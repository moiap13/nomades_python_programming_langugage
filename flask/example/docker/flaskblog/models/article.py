import os, sys
import json

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
sys.path.append(ROOT_DIR)

UPLOAD_DIR: str = os.path.join(ROOT_DIR, "static", "uploads")
CONFIG: str = os.path.join(ROOT_DIR, "config", "creds.json")

from datetime import datetime

from config.firestore_connection import DocumentReference
from helpers.gemini import GeminiAssistantService

from .user import User


class Article:
    def __init__(
        self,
        title: str,
        body: str,
        authors: list[User],
        created_at: datetime = datetime.now(),
        firestore_id: str = "",
    ):
        self.title = title
        self.body = body
        self.authors = authors
        self.created_at = created_at
        self.firestore_id = firestore_id

        with open(CONFIG) as json_config:
            config: dict[str, str] = json.load(json_config)

        self.assistant = GeminiAssistantService(config["gemini_api_key"])

    def to_dict(
        self, include_id=True
    ) -> dict[str, str | list[DocumentReference] | datetime]:
        return {
            "title": self.title,
            "body": self.body,
            "authors": [author.get_document_reference() for author in self.authors],
            "created_at": self.created_at,
        } | (
            {
                "id": self.firestore_id,
            }
            if include_id
            else {}
        )

    @staticmethod
    def from_dict(
        src: dict[str, str | list[DocumentReference] | datetime],
    ) -> "Article":
        authors_ref: list[DocumentReference] = src.get("authors", [])
        authors: list[User] = []

        for author_ref in authors_ref:
            author_data: dict[str, str | int] = author_ref.get().to_dict()
            author_id = author_ref.id
            author_data = author_data | {"id": author_id}
            authors.append(User.from_dict(author_data))

        return Article(
            title=src["title"],
            body=src["body"],
            authors=authors,
            created_at=src["created_at"],
            firestore_id=src.get("id", ""),
        )

    def verify_author(self, author_id: str) -> bool:
        # if not author_id:
        #     raise ValueError("The parameter author_id must be set")

        for author in self.authors:
            if author.firestore_id == author_id:
                return True
        return False

    def summurize_body(self) -> str:
        return self.assistant.basic_chat(
            f"""Summurize the following text: 

{self.body} 

I want minimum one sentence and maximum two sentences.
""".strip(),
            0.9,
        )
