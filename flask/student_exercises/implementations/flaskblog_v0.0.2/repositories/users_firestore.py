import os, sys

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
sys.path.append(ROOT_DIR)

import hashlib

from helpers.random_password_generator import generate_password as generate_salt
from config.firestore_config import db
from exceptions.user import UserNotFoundError
from models.user import User

class UserRepository:
  def __init__(self, collection_name: str="users"):
    self.collection_name = collection_name
    self.collection_ref = db.collection(collection_name)

  def get_user_by_uid(self, uid: str) -> User:
      # Use query alterantive instead of looping throught all the documents
      users: list[DocumentSnapshot] = self.collection_ref.where("uid", "==", uid).get()

      if len(users) > 1:
        raise ValueError(f"Many users with uid={uid}")

      if len(users) == 0:
        raise UserNotFoundError(f"user with uid={uid} not found")

      assert len(users) == 1
      return User.from_dict(users[0].to_dict() | {"firestore_id": users[0].id})

  def get_user_by_email(self, email: str) -> User:
      # Use query alterantive instead of looping throught all the documents
      users: list[DocumentSnapshot] = self.collection_ref.where("email", "==", email).get()

      if len(users) > 1:
        raise ValueError(f"Many users with email={email}")

      if len(users) == 0:
        raise UserNotFoundError(f"user with email={email} not found")

      assert len(users) == 1
      return User.from_dict(users[0].to_dict() | {"firestore_id": users[0].id})

  def get_user_by_firestore_id(self, firestore_id: str) -> User:
      if type(firestore_id) != str:
          raise ValueError("Please provide a str for parameter firestore_id")
      
      user_snapshot = self.collection_ref.document(firestore_id).get()
      if not user_snapshot.exists:
          raise UserNotFoundError("user with firestore_id={firestore_id} not found")

      return User.from_dict(user_snapshot.to_dict() | {"firestore_id": firestore_id})

# update add user to store all the user informations
  def add_user(self, user: User) -> User:
      _, doc_ref = self.collection_ref.add(user.to_dict(include_pwd=True, include_pp=True))
      user.firestore_id = doc_ref.id
      return user

  def update_user(self, user: User) -> User:
      # Update the user in the database
      self.collection_ref.document(user.firestore_id).update(user.to_dict(
        include_pp=user.pp_filename != "" 
      ))
      return self.get_user_by_firestore_id(user.firestore_id)
  
  def delete_user_pp(self, firestore_id: str) -> User:
    user_ref = self.collection_ref.document(firestore_id)
    update_data = user_ref.get().to_dict()
    if 'pp_filename' in update_data:
        update_data.pop("pp_filename")
    user_ref.set(update_data)
    return self.get_user_by_firestore_id(firestore_id)

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
    print(add_user(db, User.from_dict({
        "firstname": "Antonio",
        "lastname": "Pisanello",
        "email": "test@nomades.ch",
        "uid": "antonio",
        "pwd": "1234567890"
    })))