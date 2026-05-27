from datetime import datetime
import os, sys
ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from .user import UserRepository
from config.firestore_connection import db
from models.post import Post
from models.user import User

class PostRepository():
  def __init__(self, user_collection_name: str="posts"):
    self.collection_name = user_collection_name
    self.collection_ref = db.collection(user_collection_name)
    self.user_repository = UserRepository()

  def create(self, post: Post) -> Post:
    post_data: dict[str, str | User | datetime] = post.to_dict()
    user_ref = self.user_repository.collection_ref.document(post_data["author"].id)
    _, post_ref = self.collection_ref.add(post_data | {"author": user_ref})
    post.id = post_ref.id
    return post
  
  def get_all(self) -> list[Post]:
    post_snapshots = self.collection_ref.get()
    posts: list[Post] = []

    for post_snapshot in post_snapshots:
      post_data: dict[str, str | datetime | "DocumentReference"] = post_snapshot.to_dict()
      post_data["author"] = self.user_repository.get_by_firestore_id(post_data["author"].id)
      post_data["created_at"] = datetime.fromtimestamp(post_data["created_at"].timestamp())
      
      posts.append(Post.from_dict(post_data | {"id": post_snapshot.id}))
    
    return posts
  
  def get_my(self, user_firestore_id: str) -> list[Post]:
    # TODO: Implement the query function to retrieve all my posts from the firestore database
    # TODO: Map the retrieved docuemnt to Post object
    pass

if __name__ == '__main__':
  # Testing part
  post_repo = PostRepository()
  print(post_repo.get_all()[0].author.get_pp_ui_avatars_src())