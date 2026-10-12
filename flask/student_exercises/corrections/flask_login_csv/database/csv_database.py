import os
import sys

ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

import csv

from models.user import User

CSV_FILE: str = os.path.join(ROOT_DIR, "users.csv")


def get_user_by_username(uid: str) -> User | None:
    with open(CSV_FILE) as users_csv:
        reader = csv.DictReader(users_csv)
        for user in reader:
            if user["uid"] == uid:
                return User.from_dict(user)


def get_user_by_email(email: str) -> User | None:
    with open(CSV_FILE) as users_csv:
        reader = csv.DictReader(users_csv)
        for user in reader:
            if user["email"] == email:
                return User.from_dict(user)


def email_in_csv(email: str) -> bool:
    with open(CSV_FILE) as users_csv:
        reader = csv.DictReader(users_csv)
        for user in reader:
            if user["email"] == email:
                return True
        return False


def add_user_to_csv(user: User) -> None:
    with open(CSV_FILE, "a") as users_csv:
        writer = csv.writer(users_csv)
        writer.writerow(user.to_list(include_password=True))
