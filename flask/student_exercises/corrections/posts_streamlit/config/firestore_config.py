import os

import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.firestore import DocumentReference, DocumentSnapshot

CURR_DIR: str = os.path.dirname(__file__)
FIREBASE_JSON: str = os.path.join(CURR_DIR, "firestore-creds.json")

cred = credentials.Certificate(FIREBASE_JSON)
firebase_admin.initialize_app(cred)
db = firestore.client()