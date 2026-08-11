import os
import sys

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
CSV_FILE: str = os.path.join(ROOT_DIR, "users.csv")

sys.path.append(ROOT_DIR)

import csv
import hashlib

from firebase_admin.firestore import client

from helpers.random_password_generator import generate_password as generate_salt
from exceptions.user import UserNotFoundError

def get_user_by_uid(db: "Client", uid: str) -> dict[str, str]:
    # Use query alterantive instead of looping throught all the documents
    users: list[DocumentSnapshot] = db.collection("users").where("uid", "==", uid).get()

    if len(users) > 1:
      raise ValueError(f"Many users with uid={uid}")

    if len(users) == 0:
      raise UserNotFoundError(f"user with uid={uid} not found")

    assert len(users) == 1
    return users[0].to_dict() | {"firestore_id": users[0].id}

def get_user_by_email(db: "Client", email: str) -> dict[str, str]:
    # Use query alterantive instead of looping throught all the documents
    users: list[DocumentSnapshot] = db.collection("users").where("email", "==", email).get()

    if len(users) > 1:
      raise ValueError(f"Many users with email={email}")

    if len(users) == 0:
      raise UserNotFoundError(f"user with email={email} not found")

    assert len(users) == 1
    return users[0].to_dict() | {"firestore_id": users[0].id}

def get_user_by_firestore_id(db, firestore_id: str) -> dict[str, str]:
    if type(firestore_id) != str:
        raise ValueError("Please provide a str for parameter firestore_id")
    
    user_snapshot = db.collection("users").document(firestore_id).get()
    if not user_snapshot.exists:
        raise UserNotFoundError("user with firestore_id={firestore_id} not found")

    return user_snapshot.to_dict() | {"firestore_id": firestore_id}

# update add user to store all the user informations
def add_user(db: "Client", user: dict[str, str]) -> dict[str, str]:
    # add the user to the database using a random unique id
    salt: str = generate_salt(True, False, False, False, 10)
    user["pwd"] = hashlib.sha256((user['pwd']+salt).encode()).hexdigest()
    user["salt"] = salt
    _, doc_ref = db.collection("users").add(user)
    return user | {"firestore_id": doc_ref.id}

def update_user(db, firestore_id: str, user: dict[str, str]) -> dict[str, str]:
    # Update the user in the database
    db.collection("users").document(firestore_id).update(user)
    return get_user_by_firestore_id(db, firestore_id)
    

if __name__ == "__main__":
    import firebase_admin
    from firebase_admin import credentials, firestore
    from firebase_admin.firestore import DocumentReference, DocumentSnapshot

    FIREBASE_JSON: str = os.path.join(ROOT_DIR, "config", "firestore-creds.json")

    cred = credentials.Certificate(FIREBASE_JSON)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print(db)

    # you can add your code to test your functions
    print(add_user(db, {
        "firstname": "Antonio",
        "lastname": "Pisanello",
        "email": "test@nomades.ch",
        "uid": "antonio",
        "pwd": "1234567890"
    }))