import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.user import User
from exceptions.user import UserNotFoundError

def get_user_by_firestore_id(firestore_id: str, db: "Client") -> User:
  doc_ref = db.collection("users").document(firestore_id)
  return User.from_dict(doc_ref.get().to_dict() | {"firestore_id": firestore_id})
    
def get_user_by_uid(uid: str, db: "Client") -> User:
    """
    Function that get a unique firestore document snapshot by it's id

    Parameters
    ----------
    uid : str
        The user id

    db : Client
        The firestore client

    Returns
    -------
    dict[str, str]
        The document snapshot's data including the id
    
    Raise
    -----
    ValueError: when the user is not found
    """
    users: list["DocumentSnapshot"] = db.collection("users").where("uid", "==", uid).get()
    if len(users) == 0:
        raise UserNotFoundError(f"User with uid={uid} not exists in database")

    user_data: dict[str, str] = users[0].to_dict() | {"firestore_id": users[0].id}
    return User.from_dict(user_data)
        
def get_user_by_email(email: str, db: "Client") -> User:
    users: list["DocumentSnapshot"] = db.collection("users").where("email", "==", email).get()
    if len(users) == 0:
        raise UserNotFoundError(f"User with email={email} not exists in database")

    return User.from_dict(users[0].to_dict() | {"firestore_id": users[0].id})

def add_user(user: User, db: "Client") -> User:
    """
    Function that add a new user to the database

    Parameters
    ----------
    user : dict[str, str]
        The user's data

    db : Client
        The firestore client

    Returns
    -------
    dict[str, str]
        The user's data including the id
    """
    _, doc_ref = db.collection("users").add(user.to_dict(include_pwd=True))
    user.firestore_id = doc_ref.id
    return user

def update_user(user: User, db: "Client") -> User:
    """
    Function that update a user in the database

    Parameters
    ----------
    firestore_id : str
        The user's firestore id

    user : dict[str, str]
        The user's data

    db : Client
        The firestore client
        
    Returns
    -------
    dict[str, str]
        The user's data inlcuding the firestore id
    """
    # Update the user in the database
    db.collection("users").document(user.firestore_id).update({
      k:v for k, v in user.to_dict().items() if v != ""}
    )

    # return a dictionnary of the updated version of the user
    return get_user_by_firestore_id(user.firestore_id, db)