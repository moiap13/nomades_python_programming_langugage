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

    def get_user_by_firestore_id(self, firestore_id: str) -> User | None:
        user_snapshot: DocumentSnapshot = self.collection.document(firestore_id).get()
        if user_snapshot.exists:
            return User.from_dict(user_snapshot.to_dict() | {"id": user_snapshot.id})

    def get_user_by_username(self, uid: str) -> User | None:
        user_sanpshots: list[DocumentSnapshot] = self.collection.where(
            "uid", "==", uid
        ).get()  # GET because we expect only one result

        if len(user_sanpshots) == 1:
            return User.from_dict(
                user_sanpshots[0].to_dict() | {"id": user_sanpshots[0].id}
            )

    def get_user_by_email(self, email: str) -> User | None:
        """
        Get a user by their email from the firestore users collection
        Use where condition on email key
        """
        user_sanpshots: list[DocumentSnapshot] = self.collection.where(
            "email", "==", email
        ).get()  # GET because we expect only one result

        if len(user_sanpshots) == 1:
            return User.from_dict(
                user_sanpshots[0].to_dict() | {"id": user_sanpshots[0].id}
            )

    def email_in_database(self, email: str) -> bool:
        """
        Check if an email is in the database
        """
        return bool(self.get_user_by_email(email))

    def add_user(self, user: User) -> str:
        """
        Add a user to the database

        the user in parameter is a User object, thus he have the to_dict() method

        Return:
          firestore_id: str; the id from the firestore document database
        """
        _, docRef = self.collection.add(user.to_dict(include_password=True))
        return docRef.id


if __name__ == "__main__":
    import hashlib

    user_repo = UserRepository()

    salt: str = "AAAAAAAAAA"
    pwd = "1234567890"
    h_pwd: str = hashlib.sha256((pwd + salt).encode()).hexdigest()
    user = User("Antonio", "Pisanello", "antonio@nomades.ch", "anto", salt, h_pwd, "")
    print(user_repo.add_user(user))

    # print(user_repo.get_user_by_email("antonio@nomades.ch"))
    # print(user_repo.get_user_by_username("anto"))

    # print(user_repo.email_in_database("antonio@nomadess.ch"))
