import os
import csv
import random
from hashlib import sha256
from datetime import datetime

CURR_DIR: str = os.path.dirname(__file__)

from models.user import User
from models.post import Post
from helpers.password_generator import generate_password as generate_salt
from repositories.user import UserRepository
from repositories.post import PostRepository

user_repository = UserRepository()
post_repository = PostRepository()

cities: dict[str, dict[str, float]] = {
  # Switzerland
  "Geneva": {"lat": 46.2044, "lng": 6.1432},
  "Lausanne": {"lat": 46.5191, "lng": 6.5668},
  "Bern": {"lat": 46.9481, "lng": 7.4474},
  "Zurich": {"lat": 47.3769, "lng": 8.5417},
  "Basel": {"lat": 47.5596, "lng": 7.5886},
  "Lucerne": {"lat": 47.0502, "lng": 8.3093},
  "St. Gallen": {"lat": 47.4235, "lng": 9.3767},

  # France
  "Paris": {"lat": 48.8566, "lng": 2.3522},
  "Marseille": {"lat": 43.2965, "lng": 5.3698},
  "Lyon": {"lat": 45.7640, "lng": 4.8357},
  "Toulouse": {"lat": 43.6047, "lng": 1.4442},
  "Nice": {"lat": 43.7102, "lng": 7.2620},
  "Nantes": {"lat": 47.2184, "lng": -1.5536},

  # Italy
  "Rome": {"lat": 41.9028, "lng": 12.4964},
  "Milan": {"lat": 45.4642, "lng": 9.1900},
  "Naples": {"lat": 40.8518, "lng": 14.2681},
  "Turin": {"lat": 45.0703, "lng": 7.6869},
  "Palermo": {"lat": 40.8518, "lng": 14.2681},
  "Genoa": {"lat": 44.4056, "lng": 8.9463},

  # United state
  "New York": {"lat": 40.7128, "lng": -74.0060},
  "Los Angeles": {"lat": 34.0522, "lng": -118.2437},
  "Chicago": {"lat": 41.8781, "lng": -87.6298},
  "Houston": {"lat": 29.7604, "lng": -95.3698},
  "Phoenix": {"lat": 33.4484, "lng": -112.0740},

  # japan
  "Tokyo": {"lat": 35.6762, "lng": 139.6503},
  "Osaka": {"lat": 34.6937, "lng": 135.5023},
  "Kyoto": {"lat": 35.0116, "lng": 135.7681},
  "Hiroshima": {"lat": 34.3853, "lng": 132.4553},
}

with open(os.path.join(CURR_DIR, "posts.csv")) as post_csv_file:
  posts = csv.DictReader(post_csv_file)

  for post in posts:
    post_data: dict[str, str | User | datetime] = {}
    post_data['title'] = post["title"]
    post_data["body"] = post["body"]
    post_data["summary"] = "" # Use GeminiAssistantService to summarize when real data
    
    selected_city: dict[str, float] = random.choice(list(cities.values()))
    post_data["latlng"] = selected_city
    
    created_at_splitted:list[int] = [int(s) for s in post["created_at"].split(" ")[0].split("-")]
    create_at_date = datetime(
      created_at_splitted[0], 
      created_at_splitted[1], 
      created_at_splitted[2]
    )
    post_data["created_at"] = create_at_date

    author_name_splitted: list[str] = post["author"].split(" ")
    firstname: str = author_name_splitted[0]
    lastname: str = " ".join(author_name_splitted[1:])
    author: User = user_repository.get_by_fullname(firstname, lastname)
    post_data["author"] = author

    post: Post = post_repository.create(Post.from_dict(post_data))
    print(f"Post from {post.author.get_full_name()} inserted successfully with id={post.id}")




# with open(os.path.join(CURR_DIR, 'users.csv')) as user_csv_file:
#   users = csv.DictReader(user_csv_file, fieldnames=["firstname", "lastname"])
#   user_data: dict[str, str | int] = {}

#   for idx, user in enumerate(users, start=1):
#     user_data["firstname"] = user["firstname"]
#     user_data["lastname"] = user["lastname"]
#     user_data["uid"] = f"Student_{idx}"
#     user_data["age"] = random.randint(20, 45)
#     user_data["email"] = "student@nomades.ch"
    
#     salt: str = generate_salt(True, False, False, False, 10)
#     h_pwd: str = sha256(("1234567890"+salt).encode()).hexdigest()

#     user_data["salt"] = salt
#     user_data["pwd"] = h_pwd

#     user = user_repository.create(User.from_dict(user_data))
#     print(f"User: {user.get_full_name()} successfully created with id={user.id}")
