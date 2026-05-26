import csv


def get_user_by_uid(uid: str, csv_file: str) -> dict[str, str] | None:
    """
    Get a user by their uid

    Opens a csv file and returns the user's data

    Args:
        uid (str): The uid of the user
        csv_file (str): The path to the csv file

    Returns:
        dict[str, str] | None: The user's data
    """
    with open(csv_file, "r") as users_file:
        reader = csv.DictReader(users_file)
        for user in reader:
            if user["uid"] == uid:
                return user
