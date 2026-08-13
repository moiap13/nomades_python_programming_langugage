import os, sys

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
sys.path.append(ROOT_DIR)

import hashlib

from repositories.users_firestore import UserRepository
from models.user import User
from exceptions.user import UserNotFoundError, UserUidAlreadyExistsError, UserEmailAlreadyExistsError

from helpers.random_password_generator import generate_password as generate_salt

class UserService():
  def __init__(self):
    self._repo = UserRepository()

  def get_user_by_uid(self, uid: str) -> User:
    return self._repo.get_user_by_uid(uid)

  def get_user_by_email(self, email: str) -> User:
    return self._repo.get_user_by_email(email)

  def get_user_by_firestore_id(self, firestore_id: str) -> User:
    return self._repo.get_user_by_firestore_id(firestore_id)

  def create_user(self, user: User) -> User:
    try:
      self.get_user_by_uid(user.uid)
    except UserNotFoundError:
      pass
    else:
      raise UserUidAlreadyExistsError(f"User with uid={user.uid} already exists")
    
    try:
      self.get_user_by_email(user.email)
    except UserNotFoundError: 
        pass
    else:
        raise UserEmailAlreadyExistsError(f"User with email={user.email} already exists")

    salt: str = generate_salt(True, False, False, False, 10)
    user.pwd = hashlib.sha256((user.pwd+salt).encode()).hexdigest()
    user.salt = salt
    
    self._repo.add_user(user)
    return user

  def modify_user(self, updated_user: User) -> User:
    database_user: User = self.get_user_by_firestore_id(updated_user.firestore_id)

    if updated_user.email != database_user.email:
      try:
        self.get_user_by_email(updated_user.email)
      except UserNotFoundError:
        pass
      else:
        raise UserEmailAlreadyExistsError(f"User with email={updated_user.email} already exists")

    if updated_user.uid != database_user.uid:
      try:
        self.get_user_by_uid(updated_user.uid)
      except UserNotFoundError:
        pass
      else:
        raise UserUidAlreadyExistsError(f"User with uid={updated_user.uid} already exists")

    self._repo.update_user(updated_user)
    return updated_user

  def delete_user_pp(self, firestore_id: str):
    self._repo.delete_user_pp(firestore_id)

