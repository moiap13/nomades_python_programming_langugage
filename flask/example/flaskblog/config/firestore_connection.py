import os

import firebase_admin
from firebase_admin import credentials, firestore

CURR_DIR: str = os.path.dirname(__file__)
FIRESTORE_KEY_PATH: str = os.path.join(CURR_DIR, "firestore-creds.json")

cred = credentials.Certificate(FIRESTORE_KEY_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()
