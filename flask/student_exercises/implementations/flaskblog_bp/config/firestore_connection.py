import os

import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.firestore import DocumentSnapshot, DocumentReference

CURR_DIR = os.path.dirname(__file__)
CONFIG_FIRESTORE_PATH = os.path.join(CURR_DIR, "firestore-creds.json")

cred = credentials.Certificate(CONFIG_FIRESTORE_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()