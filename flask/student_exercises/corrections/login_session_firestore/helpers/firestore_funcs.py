from firebase_admin.firestore import client, DocumentReference, DocumentSnapshot

USERS_COLLECTION: str = 'users'

def get_user_by_uid(uid: str, db: client) -> dict[str, str | int] | None: 
  users = db.collection(USERS_COLLECTION).stream()

  for user in users:
    user_data: dict[str, str | int] = user.to_dict()
    if user_data.get("uid") == uid:
      user_data["id"] = user.id
      return user_data
