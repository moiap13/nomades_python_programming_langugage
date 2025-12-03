import os

import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.firestore import DocumentReference, DocumentSnapshot

CONFIG_DIR: str = os.path.dirname(__file__)
FIREBASE_JSON_PATH: str = os.path.join(CONFIG_DIR, "firestore-creds.json")

_cred = credentials.Certificate(FIREBASE_JSON_PATH)
firebase_admin.initialize_app(_cred)
db = firestore.client()
