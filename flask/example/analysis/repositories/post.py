from datetime import datetime
import os, sys
ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from .user import UserRepository
from config.firestore_connection import db, firestore, DocumentReference, DocumentSnapshot
from models.post import Post
from models.user import User
from mappers.post import PostMapper

class PostRepository():
  def __init__(self, user_collection_name: str="posts"):
    self.collection_name = user_collection_name
    self.collection_ref = db.collection(user_collection_name)
    self.user_repository = UserRepository()
    self.post_mapper = PostMapper()

  def create(self, post: Post) -> Post:
    post_data: dict[str, str | User | datetime] = post.to_dict()
    user_ref = self.user_repository.collection_ref.document(post_data["author"].id)
    _, post_ref = self.collection_ref.add(post_data | {"author": user_ref})
    post.id = post_ref.id
    return post
  
  def get_all(self) -> list[Post]:
    post_snapshots = self.collection_ref.order_by("created_at", direction=firestore.Query.DESCENDING).get()
    posts: list[Post] = []

    for post_snapshot in post_snapshots:
      posts.append(self.post_mapper.to_post(post_snapshot))
    
    return posts
  
  def get_my(self, user_firestore_id: str) -> list[Post]:
    # Implement the query function to retrieve all my posts from the firestore database
    user_doc_ref = self.user_repository.get_user_ref(user_firestore_id)
    post_snapshots = self.collection_ref.where("author", "==", user_doc_ref).order_by("created_at", direction=firestore.Query.DESCENDING).get()

    # Map the retrieved docuemnt to Post object
    return [self.post_mapper.to_post(post_snapshot) for post_snapshot in post_snapshots]

  def get_by_firestore_id(self, firestore_id: str) -> Post:
    post_ref: DocumentReference = self.collection_ref.document(firestore_id)
    return self.post_mapper.to_post(post_ref)
  
  def delete(self, firestore_id: str) -> None:
    self.collection_ref.document(firestore_id).delete()
  
  def get_analysis(self, authors: list[User], start_date: datetime, end_date: datetime) -> list[Post]:
    authors_ref: list[DocumentReference] = [self.user_repository.get_user_ref(author.id) for author in authors]
    post_snapshots: list[DocumentSnapshot] = self.collection_ref\
                                                    .where("author", "in", authors_ref)\
                                                    .where("created_at", ">=", start_date)\
                                                    .where("created_at", "<=", end_date)\
                                                    .get()

    return [self.post_mapper.to_post(post_snapshot) for post_snapshot in post_snapshots]

if __name__ == '__main__':
  # Testing part
  # post_repo = PostRepository()
  # print(post_repo.get_all()[0].author.get_pp_ui_avatars_src())

  db.collection("classes").document("ppl_2026_2t").collection("trascripts").add({"test": "test2"})