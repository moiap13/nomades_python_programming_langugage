import os
import sys

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
CSV_FILE: str = os.path.join(ROOT_DIR, "users.csv")

sys.path.append(ROOT_DIR)

import csv
import hashlib

from helpers.random_password_generator import generate_password as generate_salt

def get_user_by_uid(uid: str) -> dict[str, str]:
  with open(CSV_FILE) as users_csv_file:
    reader = csv.DictReader(users_csv_file)

    for user in reader:
      if user["uid"] == uid:
        return user

    return {}

def add_user(uid: str, pwd: str):
  with open(CSV_FILE, "a") as users_csv_file:
      # Add the new user to the CSV file
      writer = csv.writer(users_csv_file)
      salt: str = generate_salt(True, False, False, False, 10)
      h_pwd: str = hashlib.sha256((pwd+salt).encode()).hexdigest()
      writer.writerow([uid, salt, h_pwd])