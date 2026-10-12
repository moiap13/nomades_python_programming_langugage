import os, sys

CURR_DIR: str = os.path.dirname(__file__)
FIREBASE_CONFIG: str = os.path.join(CURR_DIR, "firestore-creds.json")
ROOT_DIR: str = os.path.dirname(CURR_DIR)

sys.path.append(ROOT_DIR)


import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.firestore import (
    DocumentReference,
    DocumentSnapshot,
    CollectionReference,
)

cred = credentials.Certificate(FIREBASE_CONFIG)
firebase_admin.initialize_app(cred)
db = firestore.client()
