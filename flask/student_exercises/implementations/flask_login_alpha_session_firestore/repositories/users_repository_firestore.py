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

def get_user_by_uid(db: "Client", uid: str) -> dict[str, str]:
    # TODO: loop throught all the document from the collection 'users'
    # TODO: CHeck that current user uid is equal to parameter uid
    # TODO: If yes, return the document data as dictionnary, with the document id in it with the firestore_id
    return {}

# update add user to store all the user informations
def add_user(db: "Client", user: dict[str, str]):
    # TODO: add the user to the database using a random unique id
    pass

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
    add_user(db, {"test": "test"})