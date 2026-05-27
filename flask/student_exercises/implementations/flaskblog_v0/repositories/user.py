import os, sys
ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from config.firestore_connection import db
from exceptions.user import UserNotFoundError
from models.user import User

class UserRepository():
  def __init__(self, user_collection_name: str="users"):
    self.collection_name = user_collection_name
    self.collection_ref = db.collection(user_collection_name)
  
  def get_by_firestore_id(self, firestore_id: str) -> User:
    user_firestore = self.collection_ref.document(firestore_id).get()
    if not user_firestore.exists:
      raise UserNotFoundError(f"User with id {firestore_id} not found")
    
    return User.from_dict(user_firestore.to_dict() | {"id": firestore_id})
  
  def update(self, user: User, remove_keys: list[str] = []) -> User:
    update_data: dict[str, str | int] = user.to_dict(True, True)
    for key in remove_keys:
      update_data.pop(key)
    
    self.collection_ref.document(user.id).update(update_data)
    return self.get_by_firestore_id(user.id)
  
  def get_by_uid(self, uid: str) -> User:
    user_snapshots = self.collection_ref.where("uid", "==", uid).get()
    if len(user_snapshots) == 0:
      raise UserNotFoundError(f"No users found with uid={uid}")
    if len(user_snapshots) > 1:
      raise ValueError(f"Many users with uid={uid}") # should never happen
    
    return User.from_dict(user_snapshots[0].to_dict() | {'id': user_snapshots[0].id})
