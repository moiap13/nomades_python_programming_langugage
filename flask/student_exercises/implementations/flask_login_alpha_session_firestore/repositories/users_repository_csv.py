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

# update add user to store all the user informations
def add_user(user: dict[str, str]):
  with open(CSV_FILE, "a") as users_csv_file:
    # Add the new user to the CSV file
    # writer = csv.DictWriter(users_csv_file, fieldnames=["firstname","lastname","email","uid","salt","pwd"])
    writer = csv.DictWriter(users_csv_file, fieldnames=user.keys())
    salt: str = generate_salt(True, False, False, False, 10)
    user["pwd"] = hashlib.sha256((user['pwd']+salt).encode()).hexdigest()
    user["salt"] = salt
    writer.writerow(user)