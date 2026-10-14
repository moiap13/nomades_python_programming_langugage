import os
import csv

CSV_FILE: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users.csv')
CSV_COLUMNS: list[str] = ["firstname", "lastname", "email", "uid", "pwd", "salt"]

def get_user_by_uid(uid: str, csv_path: str) -> dict[str, str]:
    with open(csv_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        # Loop throught the lines and check if the current line is the user's one
        for row in reader:
            # Check if password match, between users.csv password and the user's form password
            if row["uid"] == uid:
                return row
    return {}

def add_user(user: dict[str, str], csv_path: str) -> dict[str, str]:
    for key in user:
        if key not in CSV_COLUMNS:
            # TODO: adapt (not to be done in exercise :D)
            return f"Error: {key} not in {CSV_COLUMNS}"
  
    with open(csv_path, "a") as csv_file:
        # Add the new user to the CSV file
        writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)
        writer.writerow(user)
    
    return user