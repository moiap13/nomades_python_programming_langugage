from datetime import datetime
import os, sys

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
CREDS_FILE: str = os.path.join(ROOT_DIR, "config", "creds.json")
sys.path.append(ROOT_DIR)

import json

from repositories.post_firestore import PostRepository
from models.post import Post

from repositories.users_firestore import UserRepository

from AI.openrouter_provider import OpenRouterProvider

class PostService():
  def __init__(self):
    self._repo = PostRepository()
    self._user_repo = UserRepository()

    with open(CREDS_FILE) as config_file:
      config: dict[str, str] = json.load(config_file)

    self._api_key = config["openrouter_api_key"]

  def get_all(self) -> list[Post]:
    return self._repo.get_all()

  def get_my(self, firestore_id: str) -> list[Post]:
    return self._repo.get_my(firestore_id)

  def get_by_dates(self, start_date: datetime, end_date: datetime) -> list[Post]:
    return self._repo.get_by_dates(start_date, end_date)

  def get_by_author_firestore_id(self, firestore_id: str) -> Post:
    return self._repo.get_by_author_firestore_id(firestore_id)

  def create(self, post: Post) -> Post:
    summary_bot = OpenRouterProvider(self._api_key)
    post.summary = summary_bot.generate_text(
      f"You are a chief redactor of an online blog. Your task is to summarize the following post in a one sentences: {post.body}"
    )
    post.author = self._user_repo.get_user_by_firestore_id(post.author.firestore_id)
    return self._repo.create(post)

  def delete(self, firestore_id: str) -> None:
    return self._repo.delete(firestore_id)