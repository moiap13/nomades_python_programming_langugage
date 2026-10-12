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


class UserRepository:
    def __init__(self, collection_name: str = "users"):
        self.collection: CollectionReference = db.collection(collection_name)

    def get_user_by_username(self, uid: str) -> User | None:
        user_sanpshots: list[DocumentSnapshot] = self.collection.where(
            "uid", "==", uid
        ).get()
        print(user_sanpshots)

        if len(user_sanpshots) == 1:
            return User.from_dict(user_sanpshots[0].to_dict())

    def get_user_by_email(self, email: str) -> User | None:
        """
        Get a user by their email from the firestore users collection
        Use where condition on email key
        """
        # TODO: implement
        return None

    def email_in_database(self, email: str) -> bool:
        """
        Check if an email is in the database
        """
        # TODO: implement
        return False

    def add_user(self, user: User) -> str:
        """
        Add a user to the database

        the user in parameter is a User object, thus he have the to_dict() method
        """
        # TODO: implement
        return ""


if __name__ == "__main__":
    user_repo = UserRepository()
    user = user_repo.email_in_database("student@nomades.ch")
    print(user)
