from firebase_admin.firestore import DocumentReference, DocumentSnapshot
from firebase_admin.firestore import client


from .errors import UserNotFoundError


def get_user_by_uid(
    uid: str, firestore_connector: client, users_collection="users"
) -> dict[str, str | int]:
    """
    Get a user by their uid

    Args:
        uid (str): The uid of the user
        firestore_connector (client): The firestore client for communicating with database
        users_collection (str, optional): The collection name. Defaults to "users".

    Returns:
        dict[str, str]: The user's data

    Raises:
        UserNotFoundError: If the user is not found
    """
    users: list[DocumentSnapshot] = (
        firestore_connector.collection(users_collection).where("uid", "==", uid).get()
    )

    if len(users) == 0:
        raise UserNotFoundError(
            f"The user with uid={uid} not found in collection={users_collection}"
        )

    assert len(users) == 1, f"Many users with uid={uid}"

    # user_data: dict[str, str | int] = users[0].to_dict()
    # user_data.update({"id": users[0].id})
    # return user_data

    return users[0].to_dict() | {"id": users[0].id}


def get_user_by_email(
    email: str, firestore_connector: client, users_collection="users"
) -> dict[str, str | int]:
    """
    Get a user by their email

    Args:
        email (str): The email of the user
        firestore_connector (client): The firestore client for communicating with database
        users_collection (str, optional): The collection name. Defaults to "users".

    Returns:
        dict[str, str]: The user's data

    Raises:
        UserNotFoundError: If the user is not found
    """
    users: list[DocumentSnapshot] = (
        firestore_connector.collection(users_collection)
        .where("email", "==", email)
        .get()
    )

    if len(users) == 0:
        raise UserNotFoundError(
            f"The user with uid={email} not found in collection={users_collection}"
        )

    assert len(users) == 1, f"Many users with email={email}"

    return users[0].to_dict() | {"id": users[0].id}
