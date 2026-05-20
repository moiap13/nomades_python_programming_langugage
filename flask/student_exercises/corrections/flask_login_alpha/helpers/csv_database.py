import csv

def get_user_by_uid(uid: str, csv_path: str) -> dict[str, str] | None:
  with open(csv_path, "r") as users_file:
    users_rows = csv.DictReader(users_file)

    for user_row in users_rows:
        if user_row.get("uid") == uid:
           return user_row
    return None