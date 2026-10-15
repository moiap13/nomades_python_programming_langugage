import os

import firebase_admin
from firebase_admin import credentials, firestore

FIRESTORE_CREDS: str = os.path.join(os.path.dirname(__file__), "firestore-creds.json")

_cred = credentials.Certificate(FIRESTORE_CREDS)
firebase_admin.initialize_app(_cred)

db = firestore.client()