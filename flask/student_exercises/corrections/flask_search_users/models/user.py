import os

from flask import url_for

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
UPLOAD_DIR: str = os.path.join(ROOT_DIR, "static", "uploads")


class User:
    def __init__(
        self,
        firstname,
        lastname,
        uid,
        email,
        age,
        pp_filename="",
        salt="",
        pwd="",
        firestore_id="",
    ):
        self.firestore_id = firestore_id
        self.firstname = firstname
        self.lastname = lastname
        self.uid = uid
        self.email = email
        self.age = age
        self.pp_filename = pp_filename
        self.salt = salt
        self.pwd = pwd

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return (
            (
                self.firestore_id
                and other.firestore_id
                and self.firestore_id == other.firestore_id
            )
            or self.uid == other.uid
            or self.email == other.email
        )

    def to_dict(self, include_pwd=True, include_id=True) -> dict[str, str | int]:
        return (
            {
                "firstname": self.firstname,
                "lastname": self.lastname,
                "uid": self.uid,
                "email": self.email,
                "age": self.age,
                "pp_filename": self.pp_filename,
            }
            | (
                {
                    "salt": self.salt,
                    "pwd": self.pwd,
                }
                if include_pwd
                else {}
            )
            | (
                {
                    "id": self.firestore_id,
                }
                if include_id
                else {}
            )
        )

    @staticmethod
    def from_dict(src: dict[str, str | int]) -> "User":
        return User(
            firstname=src["firstname"],
            lastname=src["lastname"],
            age=src["age"],
            email=src["email"],
            uid=src["uid"],
            pp_filename=src.get("pp_filename", ""),
            pwd=src.get("pwd", ""),
            salt=src.get("salt", ""),
            firestore_id=src.get("id", ""),
        )

    def get_pp_path(self) -> str:
        pp_filename: str = self.pp_filename if self.pp_filename else "UNKNOWN"
        return (
            url_for(
                "static",
                filename=os.path.join("uploads", pp_filename),
            )
            if os.path.isfile(os.path.join(UPLOAD_DIR, pp_filename))
            else f"https://ui-avatars.com/api/?name={self.firstname}+{self.lastname}&background=random"
        )
