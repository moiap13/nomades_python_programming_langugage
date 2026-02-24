import os, sys

ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))

sys.path.append(ROOT_DIR)

from config.firestore import (
    db,
    CollectionReference,
    DocumentReference,
    DocumentSnapshot,
)
from models.user import User
from models.article import Article


class ArticleRepository:
    def __init__(self, collection_name: str = "articles"):
        self.collection = db.collection(collection_name)

    def create_article(self, article: Article) -> str:
        authors_ref: list[DocumentReference] = [
            db.document(f"users/{user.id}") for user in article.authors
        ]
        _, doc_ref = self.collection.add(article.to_dict() | {"authors": authors_ref})
        return doc_ref.id

    def get_by_firestore_id(self, firestore_id: str) -> Article:
        article_snapshot = self.collection.document(firestore_id).get()
        if article_snapshot.exists:
            article_data: dict = article_snapshot.to_dict()
            authors: list[User] = [
                (
                    User.from_dict(author.get().to_dict() | {"id": author.id})
                    if author.get().exists
                    else None
                )
                for author in article_data["authors"]
            ]
            return Article.from_dict(
                article_snapshot.to_dict() | {"authors": authors} | {"id": firestore_id}
            )

    def get_by_user(user: User) -> list[Article]:
        """
        Get all the article in the database where the user is an author

        TIPS: user the `array_contains` firestore operator

        Args:
            user (User): The user to search for

        Returns:
            list[Article]: A list of articles
        """
        # TODO: Implement this
        return []

    def delete_by_firestore_id(self, firestore_id: str) -> None:
        """
        Delete an article by its firestore id

        If the article doesn't exist, do nothing (assume it's already deleted)

        Args:
            firestore_id (str): The firestore id of the article
        """
        # TODO: Implement this
        return


if __name__ == "__main__":
    article_repository = ArticleRepository()

    # user = User("test", "", "", "", "", "", "", "")
    # article = Article("", "test", "This is a test from the repo file", [user])
    # print(article_repository.create_article(article))

    # article = article_repository.get_by_firestore_id("8npOnwe2PFlbL2zd6Y9r")
    # print(article.title)
    # print(article.body)
    # print(article.authors)
    # print(article.created_at)
    # print(article.last_modify)
    # print(article.id)
