import os

import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.firestore import DocumentReference, DocumentSnapshot

CURR_DIR: str = os.path.dirname(__file__)
FIRESTORE_CREDS = os.path.join(CURR_DIR, "firestore-creds.json")

_cred = credentials.Certificate(FIRESTORE_CREDS)
firebase_admin.initialize_app(_cred)
db = firestore.client()
