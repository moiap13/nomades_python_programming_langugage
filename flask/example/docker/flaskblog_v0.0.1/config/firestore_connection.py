import os

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import DocumentReference, DocumentSnapshot

FIRESTORE_CREDS: str = os.path.join(os.path.dirname(__file__), 'firestore-creds.json')

# Connection a firebase
_cred = credentials.Certificate(FIRESTORE_CREDS)
firebase_admin.initialize_app(_cred)# Connection a firestore
db = firestore.client()
