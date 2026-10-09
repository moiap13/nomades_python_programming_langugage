def get_user_by_firestore_id(firestore_id: str, db: "Client") -> dict[str, str]:
  doc_ref = db.collection("users").document(firestore_id)
  user_data: dict[str, str] = doc_ref.get().to_dict()
  return user_data | {"id": firestore_id}
    


def get_user_by_uid(uid: str, db: "Client") -> dict[str, str]:
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
    """
    users: list["DocumentSnapshot"] = db.collection("users").where("uid", "==", uid).get()
    if len(users) == 0:
        return {}

    return users[0].to_dict() | {"id": users[0].id}
        
def get_user_by_email(email: str, db: "Client") -> dict[str, str]:
    users: list["DocumentSnapshot"] = db.collection("users").where("email", "==", email).get()
    if len(users) == 0:
        return {}

    return users[0].to_dict() | {"id": users[0].id}


def add_user(user: dict[str, str], db: "Client") -> dict[str, str]:
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
    _, doc_ref = db.collection("users").add(user)
    firebase_id: str = doc_ref.id
    # user["id"] = firebase_id
    return user | {"id": firebase_id}
  

def update_user(firestore_id: str, user: dict[str, str], db: "Client") -> dict[str, str]:
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
    # TODO: Update the user in the database
    # TODO: return a dictionnary of the updated version of the user
    return {}