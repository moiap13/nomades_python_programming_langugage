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
from exceptions.user import UserNotFoundError


class UserRepository:
    def __init__(self, collection_name: str = "users"):
        self.collection: CollectionReference = db.collection(collection_name)

    def get_user_by_firestore_id(self, firestore_id: str) -> User:
        user_snapshot: DocumentSnapshot = self.collection.document(firestore_id).get()
        if not user_snapshot.exists:
            raise UserNotFoundError(f"User with id={firestore_id} does not exist")

        return User.from_dict(user_snapshot.to_dict() | {"id": user_snapshot.id})

    def get_user_by_username(self, uid: str) -> User:
        user_sanpshots: list[DocumentSnapshot] = self.collection.where(
            "uid", "==", uid
        ).get()  # GET because we expect only one result

        if len(user_sanpshots) != 1:
            raise UserNotFoundError(f"User with uid={uid} does not exist")

        return User.from_dict(
            user_sanpshots[0].to_dict() | {"id": user_sanpshots[0].id}
        )

    def get_user_by_email(self, email: str) -> User:
        """
        Get a user by their email from the firestore users collection
        Use where condition on email key
        """
        user_sanpshots: list[DocumentSnapshot] = self.collection.where(
            "email", "==", email
        ).get()  # GET because we expect only one result

        if len(user_sanpshots) != 1:
            raise UserNotFoundError(f"User with email={email} does not exist")

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
