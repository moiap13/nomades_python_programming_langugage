import os, sys

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
sys.path.append(ROOT_DIR)

from helpers.crypto_utils import hash_pwd

from services.user import UserService
from models.user import User
from exceptions.user import UserNotFoundError
from exceptions.login import WrongCredentialsError

class LoginService:
  def __init__(self):
    self._user_service = UserService()

  def login(self, uid_email: str, pwd: str) -> User:
    try:
      user: User = self._user_service.get_user_by_uid(uid_email)
    except UserNotFoundError:
        user: User = self._user_service.get_user_by_email(uid_email)

    if user.pwd != hash_pwd(pwd, user.salt):
      raise WrongCredentialsError

    return user
