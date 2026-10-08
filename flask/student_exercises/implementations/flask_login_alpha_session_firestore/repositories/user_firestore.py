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
    # TODO: implement


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
    # TODO: implement
  