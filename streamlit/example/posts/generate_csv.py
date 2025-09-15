import random
from datetime import datetime, timedelta
import csv
import os

# pip install wonderwords
from wonderwords import RandomSentence

CURR_DIR: str = os.path.dirname(os.path.abspath(__file__))
USER_CSV_FILE: str = os.path.join(CURR_DIR, "users.csv")
CSV_FILE: str = os.path.join(CURR_DIR, "posts.csv")

with open(USER_CSV_FILE, "r") as f:
    reader = csv.DictReader(f, delimiter="\t", fieldnames=["name", "last_name"])
    users = list(reader)


def generate_random_date(start_date: datetime, end_date: datetime) -> datetime:
    delta = end_date - start_date
    random_days: int = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


def create_articles(users: list[dict[str, str | int]]):
    sentence: RandomSentence = RandomSentence()
    start_date: datetime = datetime(2025, 5, 28)
    end_date: datetime = datetime(2025, 6, 6)

    with open(CSV_FILE, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "body", "created_at", "author"])

        for _ in range(100):
            writer.writerow(
                [
                    f"{sentence.sentence()}",
                    "\n".join(
                        [sentence.sentence() for _ in range(random.randint(5, 10))]
                    ),
                    generate_random_date(start_date, end_date),
                    " ".join(random.choice(users).values()),
                ]
            )
    print("Articles successfully generated")


create_articles(users)
